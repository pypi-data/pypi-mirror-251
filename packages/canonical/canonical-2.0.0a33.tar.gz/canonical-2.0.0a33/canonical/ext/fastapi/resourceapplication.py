# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
from types import ModuleType
from typing import get_args
from typing import get_origin
from typing import Any
from typing import Iterable
from typing import Union

import fastapi

from canonical.ext.resource import APIResourceList
from canonical.ext.resource import Error
from canonical.ext.resource import Resource
from canonical.ext.resource import ResourceInspector
from canonical.ext.resource import ResourceMeta
from canonical.ext.resource import ResourceType
from canonical.ext.resource import RootResource
from canonical.utils.http import MediaTypeSelector

from .params import NegotiateResponseMediaType
from .resourcerouter import ResourceRouter
from .response import Response


class ResourceApplication(fastapi.FastAPI):
    inspector: ResourceInspector = ResourceInspector()
    resource_paths: set[str] = set()
    media_types: MediaTypeSelector = MediaTypeSelector({
        'text/html',
        'application/json',
        'application/yaml'
    })

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.apis: dict[str, dict[str, APIResourceList]] = {}

        @self.exception_handler(404)
        def _(request: fastapi.Request, _: Any) -> Any:
            assert request.client is not None
            return Response(
                media_type=self.media_types.select(request.headers.get('Accept')),
                status_code=404,
                content=Error.factory({
                    'status_code': 404,
                    'detail': "The server cannot find the requested resource",
                    'request': {
                        'url': str(request.url),
                        'host': request.client.host
                    }
                })
            )

    def add(
        self,
        impl: type[Resource[Any] | RootResource[Any] | ResourceRouter[Any]] | ModuleType,
        verbs: Iterable[str] | None = None,
        **kwargs: Any
    ):
        self.openapi_tags = self.openapi_tags or []
        verbs = set(verbs or [])
        if inspect.isclass(impl) and issubclass(impl, ResourceRouter):
            router: ResourceRouter[Any] = impl(enabled_verbs=verbs)
            router.add_to_application(self)
            self.include_router(router=router)
        elif get_origin(impl) == Union:
            for model in get_args(impl):
                self.add(model, **kwargs)
        elif isinstance(impl, ModuleType):
            for _, value in inspect.getmembers(impl):
                if not isinstance(value, ResourceRouter):
                    continue
                value.add_to_application(self)
        else:
            router = ResourceRouter.with_model(self, impl, **kwargs) # type: ignore
            self.include_router(router=router) # type: ignore

    def create_discovery_endpoint(
        self,
        meta: ResourceMeta,
        resources: APIResourceList,
    ) -> None:

        async def discover(
            media_type: str = NegotiateResponseMediaType({'application/yaml', 'application/json', "text/html"})
        ) -> Response[Any]:
            return Response(
                status_code=200,
                media_type=media_type,
                content=self.apis[meta.api_group][meta.version]
            )

        self.add_api_route(
            methods=['GET'],
            path=f'/{resources.path(meta.api_group)}',
            endpoint=discover,
            summary="List the resources that this server supports",
            response_description="The list of resources that the server supports.",
            response_model=APIResourceList,
            include_in_schema=True,
            tags=['Service Endpoints']
        )
        

    def register_resource(self, model: type[ResourceType], verb: str) -> None:
        meta = self.inspector.inspect(model)
        if meta.api_group not in self.apis:
            self.apis[meta.api_group] = {}
        if meta.version not in self.apis[meta.api_group]:
            resources = self.apis[meta.api_group][meta.version] = APIResourceList(
                groupVersion=meta.version
            )
            self.create_discovery_endpoint(meta, resources)
        resource = model.register(self.apis[meta.api_group][meta.version])
        resource.add(verb)