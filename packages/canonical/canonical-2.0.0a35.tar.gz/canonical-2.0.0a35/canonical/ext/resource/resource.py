# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import inspect
import logging
from typing import cast
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import Literal
from typing import Self
from typing import TypeVar

import pydantic
import yaml

from canonical import ResourceName
from canonical import TypedResourceName
from canonical.exceptions import Immutable
from canonical.exceptions import Stale
from canonical.protocols import IStorage
from canonical.protocols import ITransaction
from canonical.utils import deephash
from .apiresourcelist import APIResourceList
from .listbase import ListBase
from .namespacedobjectmeta import NamespacedObjectMeta
from .objectmeta import ObjectMeta
from .objectmetabase import ObjectMetaBase
from .primarykey import PrimaryKey
from .resourcemetadata import ResourceMetadata
from .transientmeta import TransientMeta


__all__: list[str] = [
    'Resource'
]

M = ObjectMetaType = TypeVar('M', bound=ObjectMeta[Any] | TransientMeta)
S = TypeVar('S', bound='Resource[Any]')
V = TypeVar('V')
NOT_PROVIDED: object = object()


class Resource(pydantic.BaseModel, Generic[M]):
    _storage: IStorage[Self] | None = pydantic.PrivateAttr(default=None)
    List: ClassVar[type[ListBase[Any, Any]]]
    metadata_class: ClassVar[type[ObjectMeta[Any] | TransientMeta]]
    model_config = {'populate_by_name': True}
    base_path: ClassVar[str]
    group: ClassVar[str]
    logger: ClassVar[logging.Logger] = logging.getLogger('canonical.ext.resource')
    plural: ClassVar[str]
    CreateModel: ClassVar[type[Self]]
    KeyType: ClassVar[type[PrimaryKey[type[Self]]]]
    ResourceName: ClassVar[type[TypedResourceName[Any]]]
    __meta__: ClassVar[ResourceMetadata]

    api_version: str = pydantic.Field(
        default=...,
        alias='apiVersion',
        title="API Version",
        description=(
            "The `apiVersion` field defines the versioned schema of this "
            "representation of an object. Servers should convert recognized "
            "schemas to the latest internal value, and may reject "
            "unrecognized values."
        ),
        frozen=True
    )

    kind: str = pydantic.Field(
        default=...,
        description=(
            "Kind is a string value representing the REST resource this "
            "object represents. Servers may infer this from the endpoint "
            "the client submits requests to. Cannot be updated. In `CamelCase`."
        ),
        frozen=True
    )

    metadata: M = pydantic.Field(
        default=...,
        title='Metadata',
        description=(
            "`ObjectMeta` is metadata that all persisted resources "
            "must have, which includes all objects users must create."
        )
    )

    @property
    def scoped(self):
        n = self.metadata.name
        if self.is_namespaced():
            assert isinstance(self.metadata, NamespacedObjectMeta)
            n = f'{self.metadata.namespace}/{self.metadata.name}'
        return n

    @classmethod
    def is_namespaced(cls) -> bool:
        metadata_cls = cls.model_fields['metadata'].annotation
        if not inspect.isclass(metadata_cls):
             return False
        assert metadata_cls in {ObjectMeta, NamespacedObjectMeta, TransientMeta}\
            or issubclass(metadata_cls, (ObjectMeta, NamespacedObjectMeta, TransientMeta))
        return metadata_cls.is_namespaced() # type: ignore

    @classmethod
    def is_destroyable(cls) -> bool:
        """Return a boolean indicating if the resource may be destroyed
        by a client.
        """
        return True

    @classmethod
    def is_purgable(cls) -> bool:
        """Return a boolean indicating if the resources may be purged
        by a client.
        """
        return True

    @classmethod
    def new(cls, name: Any, **params: Any):
        return cls.model_validate({
            **params,
            'metadata': {
                'name': name
            }
        })

    @classmethod
    def register(cls, resources: APIResourceList):
        return resources.add(cls.__meta__)

    @property
    def key(self):
        return self.KeyType(
            name=self.metadata.name,
            namespace=getattr(self.metadata, 'name', None)
        )

    @property
    def relname(self) -> str:
        return f'{self.plural}/{self.metadata.name}'

    def __init_subclass__(cls, **kwargs: Any):
        qualname = kwargs.get('version')
        kind = kwargs.get('kind') or cls.__name__
        if qualname:
            name, version = str.split(qualname, '/')
            if '.' in name:
                cls.plural, cls.group = name.split('.', 1)
                api_version = f'{cls.group}/{version}'
            else:
                cls.group = ''
                cls.plural = name
                api_version = version

            base_path = cls.group
            if base_path:
                base_path += '/'
            base_path = f'{base_path}{version}'
            if cls.is_namespaced():
                base_path += '/namespaces/{namespace}'
            cls.base_path = f'{base_path}/{cls.plural}'

            cls.__meta__ = ResourceMetadata(
                api_group=cls.group,
                version=version,
                kind=cls.__name__,
                namespaced=cls.is_namespaced(),
                plural=cls.plural
            )

            # Set defaults and annotations.
            cls.model_fields['api_version'].annotation = Literal[api_version] # type: ignore
            cls.model_fields['api_version'].default = api_version
            cls.model_fields['kind'].annotation = Literal[kind] # type: ignore
            cls.model_fields['kind'].default = kind

            # Deprecated
            cls.ResourceName = ResourceName.subclass(cls) # type: ignore

            # Create the primary key type.
            cls.KeyType = PrimaryKey.typed(cls) # type: ignore

            # Create the list type.
            cls.List = type(f'{cls.__name__}List', (ListBase[Literal[f'{cls.__name__}List'], cls],), { # type: ignore
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

            metadata_class = cls.model_fields['metadata'].annotation
            if not inspect.isclass(metadata_class):
                return False
            assert metadata_class in {ObjectMeta, NamespacedObjectMeta, TransientMeta}\
                or issubclass(metadata_class, (ObjectMeta, NamespacedObjectMeta, TransientMeta))
            cls.metadata_class = metadata_class
            cls.model_fields['metadata'].default_factory = metadata_class.default # type: ignore

            # Create a special model for creating, updating and replacing objects.
            cls.CreateModel = type(cls.__name__, (cls,), { # type: ignore
                'model_config': {
                    'title': f'Create{cls.__name__}Request'
                },
                '__annotations__': {
                    'metadata': ObjectMetaBase
                }
            })
            cls.model_rebuild()

    def can_change(self, old: Self) -> bool:
        return True

    def get_comparison_fields(self) -> set[str]:
        return {'spec'}

    def get_mutable_data(self) -> dict[str, Any]:
        return self.model_dump(
            mode='json',
            include=self.get_mutable_fields()
        )

    def get_mutable_fields(self) -> set[str]:
        return set()

    def get_namespace(self) -> str | None:
        return self.metadata.get_namespace()

    def get_resource_name(self: S, service: str) -> TypedResourceName[S]:
        return self.ResourceName(f'//{service}/{self.plural}/{self.metadata.name}')

    def is_changed(self, old: Self) -> bool:
        a = deephash(self.model_dump(mode='json', include=self.get_comparison_fields()))
        b = deephash(old.model_dump(mode='json', include=old.get_comparison_fields()))
        return a != b

    def is_created(self):
        return bool(self.metadata.resource_version)

    def is_persistable(self) -> bool:
        return isinstance(self.metadata, (ObjectMeta, NamespacedObjectMeta))

    def model_post_init(self, _: Any) -> None:
        self.metadata.attach(self)

    def model_dump_yaml(self, indent: int =2, **kwargs: Any) -> str:
        return yaml.safe_dump(  # type: ignore
            self.model_dump(mode='json', by_alias=True, **kwargs),
            default_flow_style=False
        )

    async def persist(
        self,
        storage: IStorage[Self] | None = None,
        mode: Literal['create', 'replace'] = 'create',
        transaction: ITransaction | None = None
    ) -> Self:
        return await self.persist_key(self.key, storage, mode, transaction)

    async def persist_key(
        self,
        key: Any,
        storage: IStorage[Self] | None = None,
        mode: Literal['create', 'replace'] = 'create',
        transaction: ITransaction | None = None,
        transfer: bool = False
    ) -> Self:
        assert isinstance(self.metadata, (ObjectMeta, NamespacedObjectMeta))
        storage = storage or self._storage
        if storage is None:
            raise TypeError(
                f'{type(self).__name__} is not attached to any storage '
                'and the `storage` parameter is None.'
            )
        try:
            old = await storage.get(key)
            old.metadata.updated = datetime.datetime.now(datetime.timezone.utc)
            assert old is not None
        except storage.DoesNotExist:
            old = None

            # We are creating a new object here, so the generation
            # should be bumped to the first version.
            self.metadata.generation = 1

            # Clear any existing values for updated, uid
            self.metadata.updated = self.metadata.created
            self.metadata.uid = await storage.allocate(key.get_type()) # type: ignore

            # The deleted field can not be set on new objects,
            # because there is nothing to delete.
            if self.metadata.deleted: # type: ignore
                raise Immutable(
                    "The .metadata.deleted field must not be set on new "
                    f"{type(self).__name__} objects."
                )
        if mode == 'create' and old is not None:
            raise storage.Duplicate
        if old is not None:
            nm = cast(ObjectMeta[Any], self.metadata)
            om = cast(ObjectMeta[Any], old.metadata)
            assert isinstance(old.metadata, (ObjectMeta, NamespacedObjectMeta))

            # If the generation is non-zero, then the generation of the persisted
            # object MUST match it.
            if nm.generation and (nm.generation != om.generation):
                raise Stale

            # Same applies to the resource version.
            if nm.resource_version and (nm.resource_version != om.resource_version):
                raise Stale

            # This should never happen, but its fine to check anyway.
            if (getattr(nm, 'namespace', None) != getattr(om, 'namespace', None))\
            and not transfer:
                raise Immutable(
                    "The namespace of an object can not be changed."
                )

            # If the existing state does not allow transition to the
            # new state, throw an immutable exception.
            if not self.can_change(old):
                raise Immutable(
                    f"{type(self).__name__} does not allow the specified "
                    "changes."
                )

            # Merge the metadata of the new instance into the old instance.
            self.metadata = om.merge(nm) # type: ignore

            # Bump the generation (TODO: only bump if there are actual)
            # changes.
            if self.is_changed(old):
                self.metadata.generation += 1

        # Resource version must be updated on every write.
        self.metadata.update_resource_version(self)
        return await storage.persist(self, transaction=transaction, model=key.get_type())

    def replacable(self) -> bool:
        return True