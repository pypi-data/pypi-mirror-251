# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import cast
from typing import Annotated
from typing import TypeVar

import fastapi
import fastapi.params

from canonical.exceptions import ProgrammingError


__all__: list[str] = [
    'request_state'
]


UNSET = object()
T = TypeVar('T')


def request_state(
    name: str,
    annotation: type[T],
    required: bool = True,
    default: object = UNSET
) -> T:
    if not bool(default) ^ bool(required):
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

    return cast(T, Annotated[annotation, fastapi.Depends(f)])

