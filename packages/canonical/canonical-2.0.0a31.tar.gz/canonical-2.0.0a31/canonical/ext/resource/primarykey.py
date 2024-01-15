# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import ClassVar
from typing import Generic
from typing import TypeVar
from typing import TYPE_CHECKING

from canonical.protocols import ITyped
if TYPE_CHECKING:
    from .rootresource import ResourceType


__all__: list[str] = [
    'PrimaryKey'
]

M = TypeVar('M')


class PrimaryKey(ITyped[M], Generic[M]):
    model: type[M]
    api_group: ClassVar[str]
    plural: ClassVar[str]
    name: str
    namespace: str | None

    @classmethod
    def typed(cls, t: type['ResourceType']) -> type[ITyped[M]]:
        return type(f'{t.__name__}PrimaryKey', (cls,), {
            'api_group': t.group,
            'model': t,
            'plural': t.plural,
        })

    def __init__(
        self,
        name: str,
        namespace: str | None = None,
        server: str | None = None
    ):
        self.name = name
        self.namespace = namespace
        self.server = server

    def get_type(self) -> type[M]:
        return self.model