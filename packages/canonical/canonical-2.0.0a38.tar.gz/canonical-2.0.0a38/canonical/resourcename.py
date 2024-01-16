# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re
from typing import cast
from typing import Any
from typing import Generic
from typing import TypeVar

import pydantic

from .domainname import DomainName
from .stringtype import StringType


T = TypeVar('T', bound='ResourceName')
M = TypeVar('M', bound=pydantic.BaseModel)


class ResourceName(StringType):
    model: Any
    relname: str
    service: DomainName
    patterns = [re.compile(r'//.*')]

    @property
    def id(self) -> str:
        return str.split(self, '/')[-1]

    @property
    def kind(self) -> str:
        return str.split(self.relname, '/')[0]

    @classmethod
    def null(cls: type[T]) -> T: # pragma: no cover
        """Return an instance that represents an unassigned
        resource name.
        """
        return cls('//cochise.io/_/null')

    @classmethod
    def subclass(cls, model: type[Any]):
        return type(f'{model.__name__}Name', (cls,), {}, model=model)

    def __new__(
        cls: type[T],
        object: str,
        service: DomainName | None = None,
        relname: str | None = None
    ) -> T:
        self = super().__new__(cls, object) # type: ignore
        if service is None:
            # Was not created by pydantic
            for validator in cls.__get_validators__():
                self = validator(self)
        else:
            assert relname is not None
            self.relname = relname
            self.service = service
        return cast(T, self)

    def __init_subclass__(cls, model: type[Any]) -> None:
        super().__init_subclass__()
        cls.model = model

    @classmethod
    def validate(cls, v: str, _: Any = None) -> str:
        v = super().validate(v, _)
        assert str.startswith(v, '//')
        service, _, relname = str.partition(v[2:], '/')
        if not relname:
            raise ValueError("a valid ResourceName contains a relative name.")
        for validator in DomainName.__get_validators__():
            service = validator(service)
        return cls(v, relname=relname, service=DomainName(service))


class TypedResourceName(ResourceName, Generic[M], model=pydantic.BaseModel):
    model: type[M]