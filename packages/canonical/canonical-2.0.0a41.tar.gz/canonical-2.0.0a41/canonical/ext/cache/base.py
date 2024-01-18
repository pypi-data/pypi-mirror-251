# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import hashlib
import json
import logging
from typing import Any, Literal
from typing import TypeVar

import pydantic

from canonical.lib.protocols import ICache


T = TypeVar('T')

class BaseCache(ICache):
    __module__: str = 'canonical.ext.cache'
    logger: logging.Logger = logging.getLogger('canonical.ext.cache')

    def __init__(self, keyalg: Literal['sha256'] | None = None):
        self.keyalg = keyalg

    def hash(self, value: str, algorithm: str | None = None) -> str:
        algorithm = algorithm or self.keyalg
        if algorithm is None:
            return value
        h = hashlib.new(algorithm)
        h.update(str.encode(value))
        return h.hexdigest()

    def serialize(self, value: T, encoder: type[T]) -> bytes:
        adapter = pydantic.TypeAdapter[T](encoder)
        return adapter.dump_json(value)

    def deserialize(self, value: bytes , decoder: type[T], mode: str) -> T:
        adapter = pydantic.TypeAdapter[T](decoder)
        match mode:
            case 'json':
                result = adapter.validate_python(json.loads(value))
            case 'python':
                result = adapter.validate_python(value)
            case _:
                raise NotImplementedError(mode)
        return result

    async def clear(self, key: str) -> None:
        raise NotImplementedError

    async def fetch(self, key: str) -> bytes | None:
        raise NotImplementedError

    async def get(
        self,
        key: str,
        decoder: type[T] = bytes,
        validation: Literal['strict', 'ignore'] = 'strict',
        mode: Literal['json'] = 'json',
        keyalg: Literal['sha256'] | None = None
    ) -> T | None:
        key = self.hash(key, algorithm=keyalg)
        value = await self.fetch(key)
        if value is None:
            self.logger.debug(
                "Cache did not contain the request key (key: %s).",
                key
            )
            return None
        try:
            return self.deserialize(value, decoder, mode)
        except (pydantic.ValidationError, ValueError, TypeError):
            if validation == 'strict':
                raise
            await self.clear(key)
            return None

    async def set(
        self,
        key: str,
        value: Any,
        encoder: type[T] = bytes,
        encrypt: bool = False,
        ttl: int | None = None,
        keyalg: Literal['sha256'] | None = None
    ) -> None:
        await self.put(
            key=key,
            value=self.serialize(value, encoder),
            encrypt=encrypt,
            ttl=ttl
        )
        