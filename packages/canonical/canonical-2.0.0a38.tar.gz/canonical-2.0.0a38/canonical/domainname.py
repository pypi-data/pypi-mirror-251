# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import re
from typing import Any
from typing import Callable
from typing import Generator
from typing_extensions import SupportsIndex

from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema
from pydantic_core import core_schema


class DomainName(str):
    __module__: str = 'canonical'
    pattern: re.Pattern[str] = re.compile(r'^([0-9a-z\-_]+)$')

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        _: CoreSchema,
        handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return handler(core_schema.str_schema(max_length=2048))

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., str | None], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any, _: Any = None) -> str:
        if not isinstance(v, str):
            raise ValueError(f"Can not create DomainName from {type(v).__name__}")
        if not v:
            raise ValueError("A domain name can not be an empty string.")
        if len(v) > 253:
            raise ValueError("Value is too long to be a valid domain name.")
        v = str.lower(v)
        labels: list[str] = str.split(v, '.')
        for label in labels:
            if label.startswith('-') or label.endswith('-'):
                raise ValueError("A DNS label can not start or end with a hyphen.")
            if not cls.pattern.match(label):
                raise ValueError("Invalid characters in DNS label.")
            if len(label) > 63:
                raise ValueError("A DNS label is at most 63 characters.")
        return cls(v)

    def __getitem__(self, __i: SupportsIndex | slice) -> str:
        value = str.split(self, '.')[__i]
        if isinstance(value, list):
            value = str.join('.', value)
        return value