# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
from typing import Any
from typing import Generic
from typing import Self
from typing import TypeVar
from typing import TYPE_CHECKING

import pydantic

from canonical.utils import deephash
if TYPE_CHECKING:
    from .resource import Resource
from .resourcekey import ResourceKey


N = TypeVar('N')
ObjectMetaType = N


class ObjectMetaBase(pydantic.BaseModel, Generic[N]):
    model_config = {'populate_by_name': True, 'title': 'ObjectMeta'}
    _namespace: bool = pydantic.PrivateAttr(default=False)
    _version: str = pydantic.PrivateAttr()
    _kind: str = pydantic.PrivateAttr()

    annotations: dict[str, Any] = pydantic.Field(
        default_factory=dict,
        title="Annotations",
        description=(
            "Annotations is an unstructured key value map stored with "
            "a resource that may be set by external tools to store "
            "and retrieve arbitrary metadata. They are not queryable and "
            "should be preserved when modifying objects."
        )
    )

    finalizers: set[str] = pydantic.Field(
        default_factory=set,
        description=(
            "Must be empty before the object is deleted from the registry. "
            "Each entry is an identifier for the responsible component that "
            "will remove the entry from the list. If the `deleted` field "
            "of the object is non-nil, entries in this list can only be "
            "removed. Finalizers may be processed and removed in any order."
        )
    )

    labels: dict[str, str | None] = pydantic.Field(
        default_factory=dict,
        title="Labels",
        description=(
            "Map of string keys and values that can be used to organize and "
            "categorize (scope and select) objects."
        )
    )

    name: N = pydantic.Field(
        default=...,
        title="Name",
        description=(
            "Name must be unique within a namespace. Is required when creating "
            "resources, although some resources may allow a client to request "
            "the generation of an appropriate name automatically. Name is "
            "primarily intended for creation idempotence and configuration "
            "definition. Cannot be updated."
        ),
        frozen=True
    )

    generate_name: str | None = pydantic.Field(
        default=None,
        alias='generateName',
        description=(
            "An optional prefix, used by the server, to generate a unique name "
            "ONLY IF the `name` field has not been provided. If this field "
            "is used, the name returned to the client will be different than "
            "the name passed. This value will also be combined with a unique "
            "suffix. The provided value has the same validation rules as the "
            "`name` field, and may be truncated by the length of the suffix "
            "required to make the value unique on the server. If this field "
            "is specified and the generated name exists, the server will "
            "return a 409. Applied only if `name` is not specified."
        ),
        exclude=True
    )

    tags: set[str] = pydantic.Field(
        default_factory=set,
        description=(
            "An array of tags that may be used to classify an object "
            "if a label or annotation is not applicable."
        )
    )

    @property
    def key(self) -> ResourceKey[N]:
        return ResourceKey(api_version=self._api_version, kind=self._kind, name=self.name)

    @classmethod
    def is_namespaced(cls) -> bool:
        return False

    @classmethod
    def default(cls) -> 'ObjectMetaBase[Any]':
        raise ValueError("Can not create ObjectMetaBase without parameters.")

    @classmethod
    def __pydantic_init_subclass__(cls, namespaced: bool = False, **kwargs: Any) -> None:
        cls._namespaced = namespaced

    def attach(self, resource: Resource[Any]):
        self._api_version = resource.api_version
        self._kind = resource.kind

    def get_namespace(self) -> str | None:
        return None

    def is_labeled(self, names: list[str]) -> bool:
        return all([
            self.labels.get(name) not in {None, 'null'}
            for name in names
        ])

    def merge(self, metadata: Self):
        """Merge :class:`ObjectMeta` `metadata` into this instance."""
        # Only annotations, labels and tags are merged for now.
        self.annotations = {**self.annotations, **metadata.annotations}
        self.labels = {**self.labels, **metadata.labels}
        self.tags = {*self.tags, *metadata.tags}
        return self

    def update_resource_version(self, obj: pydantic.BaseModel):
        data = obj.model_dump(
            mode='json',
            exclude={'api_version', 'kind'}
        )
        self.resource_version = deephash(data, encode='hex')