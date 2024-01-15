# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import overload
from typing import Any
from typing import NoReturn
from typing import TypeVar

import httpx
import pydantic
from fastapi.exceptions import HTTPException

from canonical.ext.iam import PermissionQuery
from canonical.ext.iam import PermissionSet
from canonical.ext.iam.types import Permission
from canonical.ext.resource import APIResource
from canonical.ext.resource import APIResourceList
from canonical.ext.resource import ResourceType
from canonical.ext.httpx import AsyncClient
from canonical.ext.resource import Error


R = TypeVar('R', bound=ResourceType)
T = TypeVar('T', bound=pydantic.BaseModel)


class ResourceClient(AsyncClient):
    _supported_resources: dict[str, APIResourceList] = {}

    def can_retry_timeout(self, request: httpx.Request):
        return super().can_retry_timeout(request) or any([
            str.endswith(request.url.path, ':permissions')
        ])

    def construct_uri(
        self,
        group: str,
        kind: str,
        name: str | None = None,
        namespace: str | None = None,
        version: str | None = None
    ):
        version = version or 'v1'
        url = f'{version}/{kind}'
        if group:
            url = f'{group}/{url}'
        if namespace is not None:
            url = f'/{group}/{version}/namespaces/{namespace}/{kind}'
        if name is not None:
            url = f'{url}/{name}'
        return url

    def is_discovered(self, api_version: str) -> bool:
        return api_version in self._supported_resources

    def raise_for_status(self, response: httpx.Response) -> NoReturn | None:
        if response.status_code >= 400:
            error = Error.model_validate_json(response.content)
            raise HTTPException(
                status_code=error.data.status_code,
                detail=error.data.detail
            )

    @overload
    def resource_factory(self, model: None, response: httpx.Response) -> dict[str, Any]:
        ...

    @overload
    def resource_factory(self, model: type[T], response: httpx.Response) -> T:
        ...

    def resource_factory(self, model: type[T] | None, response: httpx.Response) -> T | dict[str, Any]:
        return (
            response.json()
            if not model else
            model.model_validate_json(response.content)
        )

    async def apply(self, obj: dict[str, Any]) -> None:
        """Applies the given specification to the system."""
        metadata: dict[str, Any] | Any = obj.get('metadata')
        if metadata is None or not isinstance(metadata, dict):
            raise TypeError(
                "The metadata field is required and must be a "
                "dictionary."
            )
        name = metadata.get('name')
        generate = bool(metadata.get('generateName'))
        ns = metadata.get('namespace')
        if (name is None or not isinstance(name, (str, int))) and not generate:
            raise TypeError(
                "The .metadata.name field is required and must be a "
                "string."
            )
        resource, api_version = await self.discover(obj)
        if (ns is None or not isinstance(ns, str)) and resource.namespaced:
            raise TypeError(
                "The metadata.namespace field is required and must be a "
                "string."
            )
        method = self.create
        if name:
            method = self.replace
            exists = await self.exists(
                resource.path(
                    api_version=api_version,
                    name=name,
                    namespace=ns
                )
            )
            if not exists:
                method = self.create
            result = await method(resource, api_version, ns, name, obj)
        else:
            result = await method(resource, api_version, ns, name, obj)
        return result

    async def create(
        self,
        resource: APIResource,
        api_version: str,
        namespace: str | None,
        name: str | int | None,
        obj: dict[str, Any]
    ) -> None:
        response = await self.post(
            url=resource.path(api_version, namespace=namespace),
            json=obj
        )
        response.raise_for_status()

    async def discover(self, obj: dict[str, Any]):
        api_version: str | None = obj.get('apiVersion')
        if api_version is None:
            raise TypeError("The apiVersion field is required.")
        kind = obj.get('kind')
        if kind is None:
            raise TypeError("The kind field is required.")
        if not self.is_discovered(api_version):
            response = await self.get(
                url=api_version,
                headers={'Accept': 'application/json'}
            )
            response.raise_for_status()
            self._supported_resources[api_version] = APIResourceList\
                .model_validate_json(response.content)

        return self._supported_resources[api_version].get(kind), api_version

    async def exists(self, url: str) -> bool:
        response = await self.head(
            url=url,
            follow_redirects=True
        )
        if response.status_code not in {200, 404}:
            response.raise_for_status()
        return response.status_code == 200

    async def permissions(
        self,
        namespace: str | None,
        permission: str,
        *permissions: str,
        **kwargs: Any
    ) -> set[Permission]:
        """Retrieve the permissions that the client has on the given
        resource.
        """
        query = PermissionQuery.factory({
            'permissions': {permission, *permissions}
        })
        headers: dict[str, str] = kwargs.setdefault('headers', {})
        headers.setdefault('Accept', 'application/json')
        response = await self.post(
            headers=headers,
            url=f"{self.construct_uri('', 'namespaces', namespace)}:permissions",
            json=query.model_dump(by_alias=True, mode='json')
        )
        self.raise_for_status(response)
        result = PermissionSet.model_validate_json(response.content)
        return {Permission(x) for x in result.granted}

    @overload
    async def request_resource(self, model: None, **kwargs: Any) -> dict[str, Any]:
        ...

    @overload
    async def request_resource(self, model: type[T], **kwargs: Any) -> T:
        ...

    async def request_resource(self, model: type[T] | None, method: str, **kwargs: Any) -> T | dict[str, Any]:
        headers = kwargs.setdefault('headers', {})
        headers['Accept'] = 'application/json'
        response = await self.request(method=method, **kwargs)
        self.raise_for_status(response)
        resource = response.json()
        if model is not None:
            resource = self.resource_factory(model, response)
        return resource

    async def retrieve(
        self,
        group: str,
        kind: str,
        name: str,
        model: type[T] | None = None,
        namespace: str | None = None,
        version: str | None = None,
    ) -> dict[str, Any] | T:
        return await self.request_resource(
            model=model,
            method='GET',
            url=self.construct_uri(group, kind, name, namespace, version)
        )

    async def replace(
        self,
        resource: APIResource,
        api_version: str,
        namespace: str | None,
        name: str | int,
        obj: dict[str, Any]
    ) -> None:
        response = await self.put(
            url=resource.path(api_version, name=name, namespace=namespace),
            json=obj
        )
        response.raise_for_status()