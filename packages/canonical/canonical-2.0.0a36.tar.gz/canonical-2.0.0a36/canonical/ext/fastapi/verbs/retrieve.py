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

from ..params import ResourceRepository
from ..params import RequestAuthorizationContext
from ..params import RequestResourceName
from .default import Default


T = TypeVar('T')


class Retrieve(Default[T]):
    detail = True
    existing = True
    method = 'GET'
    status_code = 200
    verb = 'get'


    async def handle( # type: ignore
        self,
        ctx: RequestAuthorizationContext,
        repo: ResourceRepository,
        key: RequestResourceName,
    ) -> bool:
        if not ctx.is_authenticated() or not ctx.is_authorized():
            return False
        raise NotImplementedError

    async def render_to_response(self, result: bool) -> fastapi.Response: # type: ignore
        return fastapi.Response(
            status_code=200 if result else 404
        )

    def get_endpoint_summary(self) -> str:
        return f'Retrieve a specific {self.model.__name__}'

    def get_response_description(self) -> str:
        return f"{self.model.__name__} object."