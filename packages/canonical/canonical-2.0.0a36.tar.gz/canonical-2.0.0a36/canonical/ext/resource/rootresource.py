# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import get_args
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import Literal
from typing import Self
from typing import TypeAlias
from typing import TypeVar

import pydantic

from canonical import ResourceName
from canonical import TypedResourceName
from .apiresourcelist import APIResourceList
from .listbase import ListBase
from .primarykey import PrimaryKey
from .resource import Resource
from .resourcemetadata import ResourceMetadata

__all__: list[str] = [
    'RootResource'
]

T = TypeVar('T', bound=Resource[Any])
S = TypeVar('S', bound='RootResource[Any]')


class RootResource(pydantic.RootModel[T], Generic[T]):
    _is_namespaced: bool
    group: ClassVar[str]
    base_path: ClassVar[str]
    plural: ClassVar[str]
    List: ClassVar[type[ListBase[Any, Any]]]
    KeyType: ClassVar[type[PrimaryKey[type[Self]]]]
    CreateModel: ClassVar[type[Self]]
    ResourceName: ClassVar[type[TypedResourceName[Any]]]
    __meta__: ClassVar[ResourceMetadata]

    @property
    def api_version(self):
        return self.root.api_version

    @property
    def key(self) -> PrimaryKey[type[Self]]:
        return self.KeyType(
            name=self.metadata.name,
            namespace=getattr(self.metadata, 'namespace', None)
        )

    @property
    def kind(self):
        return self.root.kind

    @property
    def metadata(self):
        return self.root.metadata

    @property
    def relname(self):
        return self.root.relname

    @classmethod
    def register(cls, resources: APIResourceList):
        return resources.add(cls.__meta__)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any):
        paths: set[str] = set()
        types: tuple[Resource[Any]] = get_args(cls.model_fields['root'].annotation) # type: ignore
        for model in types:
            paths.add(model.base_path)
        if len(paths) > 1:
            raise ValueError(f"All root models must have the same base path.")
        if paths:
            assert len(types) > 1
            cls.base_path = types[0].base_path
            cls.group = types[0].group
            cls.plural = types[0].plural
            cls._namespaced = types[0].is_namespaced()
            cls.KeyType = PrimaryKey.typed(cls) # type: ignore
            cls.__meta__ = ResourceMetadata.model_validate({
                **types[0].__meta__.model_dump(),
                'kind': cls.__name__
            })
        cls.ResourceName = ResourceName.subclass(cls) # type: ignore
        cls.List = type(f'{cls.__name__}List', (ListBase[Literal[f'{cls.__name__}List'], cls],), {
            'items': pydantic.Field(
                default_factory=list,
                description=(
                    "The `items` member contains an array "
                    f"of `{cls.__name__}` objects."
                )
            ),
            '__annotations__': {'items': list[cls]}
        })
        cls.List.model_fields['kind'].default = f'{cls.__name__}List'
        cls.List.model_rebuild()

        cls.model_config.update({
            'title': cls.__name__
        })
        cls.model_rebuild()

    @classmethod
    def is_destroyable(cls) -> bool:
        return True

    @classmethod
    def is_namespaced(cls) -> bool:
        return cls._is_namespaced

    @classmethod
    def is_purgable(cls) -> bool:
        return True

    def can_change(self, old: T) -> bool:
        return self.root.can_change(old)

    def get_comparison_fields(self) -> set[str]:
        return self.root.get_comparison_fields()

    def get_namespace(self) -> str | None:
        return self.root.get_namespace()

    def get_resource_name(self: S, service: str) -> TypedResourceName[S]:
        return self.ResourceName(self.root.get_resource_name(service))

    def model_dump_yaml(self, **kwargs: Any):
        return self.root.model_dump_yaml(**kwargs)

    def replacable(self) -> bool:
        return self.root.replacable()

    async def persist(self, *args: Any, **kwargs: Any):
        obj = await self.root.persist_key(self.key, *args, **kwargs)

        # Ensure that the same type is returned.
        return self.model_validate(obj.model_dump())


ResourceType: TypeAlias = Resource[Any] | RootResource[Any]
ResourceTypeVar = TypeVar('ResourceTypeVar', bound=ResourceType)