# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from canonical.ext.fastapi.params import RequestAuthorizationContext

import fastapi

from ..params import ResourceRepository
from ..params import RequestResourceName
from .default import Default


class Exists(Default[[RequestAuthorizationContext, ResourceRepository, RequestResourceName], bool]):
    detail = True
    existing = False
    method = 'HEAD'
    status_code = 200
    verb = 'exists'

    async def authorize(self) -> None: # type: ignore
        pass

    async def exists(
        self,
        repo: ResourceRepository,
        key: RequestResourceName
    ) -> bool:
        return await repo.exists(key)

    async def handle(
        self,
        ctx: RequestAuthorizationContext,
        repo: ResourceRepository,
        key: RequestResourceName,
    ) -> bool:
        if not ctx.is_authenticated() or not ctx.is_authorized():
            return False
        return await self.exists(repo, key)

    async def render_to_response(self, result: bool) -> fastapi.Response:
        return fastapi.Response(
            status_code=200 if result else 404
        )

    def get_endpoint_summary(self) -> str:
        return f'Check if {self.model.__name__} exists'

    def get_openapi_responses(self) -> dict[int, dict[str, Any]]:
        return {
            **super().get_openapi_responses(),
            200: {
                'description': self.get_response_description()
            }
        }

    def get_response_description(self) -> str:
        return f'The {self.model.__name__} specified by the path parameter(s) exists.'