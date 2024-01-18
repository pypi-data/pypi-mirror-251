# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from collections import OrderedDict
from inspect import Parameter
from inspect import Signature
from typing import Any
from typing import TypeVar

from canonical.ext.resource import Error
from canonical.ext.resource import Resource
from canonical.ext.resource import RootResource
from ..response import Response
from .default import Default


T = TypeVar('T', bound=Resource[Any] | RootResource[Any])


class Create(Default[T]):
    creates = True
    detail = False
    exists = False
    method = 'POST'
    requires_body = True
    status_code = 201
    verb = 'create'

    def annotate_handler(self, signature: Signature) -> Signature:
        params: OrderedDict[str, Parameter] = OrderedDict(signature.parameters)
        for name, param in signature.parameters.items():
            if param.annotation == self.model:
                params[name] = param.replace(annotation=self.get_input_model())
                self.input_params.add(name)
                continue

        return signature.replace(parameters=list(params.values()))

    def get_endpoint_summary(self) -> str:
        return f'Create a new {self.model.__name__}'

    def get_openapi_responses(self) -> dict[int, dict[str, Any]]:
        return {
            **super().get_openapi_responses(),
            409: {
                'model': Error,
                'description': (
                    f'Conflicts with an existing {self.model.__name__} object.'
                )
            }
        }

    def get_response_description(self) -> str:
        return f'The created {self.model.__name__} object.'

    async def render_to_response(
        self,
        result: Any
    ) -> Response[Any]:
        if not isinstance(result, (Resource, RootResource)):
            raise TypeError(
                "Function handle() must return a Resource or RootResource "
                "instance."
            )
        return Response(
            status_code=201,
            content=result
        )