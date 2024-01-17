# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
from collections import OrderedDict
from typing import get_origin
from typing import Any
from typing import Annotated

import fastapi
import fastapi.params

from canonical.exceptions import ProgrammingError


__all__: list[str] = [
    'request_state'
]


UNSET = object()


def request_state(
    name: str,
    annotation: Any,
    required: bool = True,
    default: object = UNSET
) -> Any:
    if not bool(default != UNSET) ^ bool(required):
        raise TypeError(
            "The `required` and `default` parameters are mutually "
            "exclusive."
        )

    def f(request: fastapi.Request):
        v = getattr(request, name, default)
        if v == UNSET and required:
            raise ProgrammingError(
                f"Dependency requires request.state.{name} "
                "to be present."
            )
        setattr(request.state, name, v)
        return v

    return fastapi.Depends(f)




def inject(*args: Any, **kwargs: Any):
    def f(request: fastapi.Request, **kwargs: Any):
        for k, v in kwargs.items():
            setattr(request.state, k, v)

    sig = inspect.signature(f)
    params: OrderedDict[str, inspect.Parameter] = OrderedDict([
        ('request', sig.parameters['request'])
    ])
    for i, dependency in enumerate(args):
        name = f'__arg_{i}'
        if isinstance(dependency, fastapi.params.Depends):
            kwargs[name] = dependency
            continue
        if not get_origin(dependency) == Annotated:
            continue
        params[name] = inspect.Parameter(
            kind=inspect.Parameter.POSITIONAL_ONLY,
            name=name,
            annotation=dependency
        )
        
    for name, dependency in kwargs.items():
        if not isinstance(dependency, fastapi.params.Depends):
            dependency = fastapi.params.Depends(dependency)
        params[name] = inspect.Parameter(
            kind=inspect.Parameter.KEYWORD_ONLY,
            name=name,
            default=dependency,
            annotation=Any
        )
    setattr(f, '__signature__', sig.replace(parameters=list(params.values())))
    return [fastapi.Depends(f)]