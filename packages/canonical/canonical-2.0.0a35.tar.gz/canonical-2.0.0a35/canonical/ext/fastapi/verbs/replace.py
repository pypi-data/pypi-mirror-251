# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar

import fastapi

from canonical.ext.resource import Error
from canonical.ext.resource import IResourceRepository
from canonical.ext.resource import ResourceType
from canonical.ext.iam.protocols import IResourceAuthorizationContext
from ..response import Response
from .detail import Detail


T = TypeVar('T')


class Replace(Detail[T]):
    detail = True
    existing = True
    method = 'PUT'
    requires_body = True
    verb = 'replace'

    def can_replace(self, resource: ResourceType) -> bool:
        return resource.replacable()

    def get_endpoint_summary(self) -> str:
        return f'Replace an existing {self.model.__name__}'

    def get_openapi_responses(self) -> dict[int, Any]:
        return {
            **super().get_openapi_responses(),
            409: {
                'model': Error,
                'description': (
                    f'The {self.model.__name__} identified by the path parameters '
                    'can not be replaced.'
                )
            }
        }

    def get_response_description(self) -> str:
        return f"The latest version of the {self.model.__name__} object."

    async def on_mutation_request(
        self,
        request: fastapi.Request,
        ctx: IResourceAuthorizationContext,
        repo: IResourceRepository,
        resource: Any
    ) -> None:
        if not self.can_replace(resource):
            self.fail(409, f"{self.model.__name__} can not be replaced in its current state.")

    async def render_to_response(self, result: Any) -> Response[Any]:
        if not isinstance(result, self.model):
            raise TypeError(
                f"Function handle() must return a {self.model.__name__} "
                f"instance, got {type(result).__name__}."
            )
        return Response(
            status_code=205,
            content=result
        )