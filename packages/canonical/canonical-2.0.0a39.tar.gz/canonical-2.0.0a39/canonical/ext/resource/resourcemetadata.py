# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
import inspect
from typing import Any
from typing import Literal
from typing import TYPE_CHECKING

import pydantic
from pydantic.fields import FieldInfo

from .primarykey import PrimaryKey
if TYPE_CHECKING:
    from .resource import Resource
    from .rootresource import RootResource


class ResourceMetadata(pydantic.BaseModel):
    _create_model: type[pydantic.BaseModel] = pydantic.PrivateAttr()
    api_group: str
    version: str
    kind: str
    namespaced: bool
    plural: str

    @classmethod
    def fromqualname(cls, model: type[Resource[Any] | RootResource[Any]], qualname: str):
        name, version = str.split(qualname, '/')
        if '.' in name:
            plural, group = name.split('.', 1)
        else:
            group = ''
            plural = name
        return cls(
            api_group=group,
            version=version,
            kind=model.__name__,
            namespaced=model.is_namespaced(),
            plural=plural
        )

    @property
    def api_version(self) -> str:
        return f'{self.api_group}/{self.version}'\
            if self.api_group\
            else self.version

    def contribute_to_class(
        self,
        cls: type[Resource[Any] | RootResource[Any]],
        fields: dict[str, FieldInfo]
    ):
        cls.__meta__ = self
        cls.group = self.api_group
        cls.plural = self.plural
        base_path = self.api_group
        if base_path:
            base_path += '/'
        base_path = f'{base_path}{self.version}'
        if cls.is_namespaced():
            base_path += '/namespaces/{namespace}'
        cls.base_path = f'{base_path}/{self.plural}'

        # Set defaults and annotations.
        if fields:
            fields['api_version'].annotation = Literal[f'{self.api_version}']
            fields['api_version'].default = self.api_version
            fields['kind'].annotation = Literal[f'{self.kind}']
            fields['kind'].default = self.kind

            # Find the metadata class
            metadata_class = fields['metadata'].annotation
            if not inspect.isclass(metadata_class):
                raise NotImplementedError
            metadata_class.add_to_model(cls)

        cls.KeyType = PrimaryKey.typed(cls) # type: ignore
        #assert cls.model_rebuild(force=True)
        