# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import functools
from typing import cast
from typing import Any
from typing import AsyncIterable

from google.cloud.datastore import Client

from canonical.protocols import ITransaction
from canonical.protocols import ITyped
from canonical.ext.resource import IResourceRepository
from canonical.ext.resource import PrimaryKey
from canonical.ext.resource import ResourceType
from canonical.ext.resource import ResourceTypeVar
from .basedatastorestorage import BaseDatastoreStorage
from .protocols import IDatastoreKey
from .protocols import IDatastoreEntity


class ResourceRepository(BaseDatastoreStorage, IResourceRepository):
    cluster_namespace: str

    async def allocate(self, resource: ResourceType) -> int:
        return await self.allocate_identifier(resource.kind)

    def all(
        self,
        model: type[ResourceTypeVar],
        namespace: str | None = None
    ) -> AsyncIterable[ResourceTypeVar]:
        return self.query( # type: ignore
            model=model,
            namespace=namespace
        )

    def get_entity_name(self, cls: type[ResourceType]) -> str:
        name = f'{cls.group}/{cls.__name__}'
        if not cls.group:
            name = cls.__name__
        return name

    def resource_key(self, resource: ResourceType, model: type[ResourceType] | None = None) -> IDatastoreKey:
        args: list[Any] = [self.get_entity_name(model or type(resource)), resource.metadata.name]
        return self.client.key(*args, namespace=resource.get_namespace()) # type: ignore

    async def exists(self, key: ITyped[ResourceType]) -> bool:
        assert isinstance(key, PrimaryKey)
        print(key.name, key.namespace)
        filters: list[tuple[str, str, Any]] = [
            ('metadata.name', '=', key.name)
        ]
        if key.namespace is not None:
            filters.append(('metadata.namespace', '=', key.namespace))
        q = self.query(model=key.model, filters=filters)
        return await q.exists()

    async def get(
        self,
        key: ITyped[Any],
        cached: bool = False,
        model: type[ResourceType] | None = None,
        max_age: int = 0,
        transaction: ITransaction | None = None,
        **kwargs: Any
    ) -> ResourceType:
        key = cast(PrimaryKey[ResourceType], key)
        if cached:
            raise NotImplementedError
        obj = await self.get_model_by_key(
            cls=key.get_type(),
            pk=key.name
        )
        if obj is None:
            raise self.DoesNotExist
        return obj

    async def get_by_name(
        self,
        model: type[ResourceType],
        name: str | int,
        namespace: str | None = None
    ) -> ResourceType:
        obj = await self.get_model_by_key(model, name, namespace=namespace)
        if obj is None:
            raise self.DoesNotExist
        return obj

    async def persist_entity(
        self,
        client: Client | ITransaction,
        entity: IDatastoreEntity
    ) -> IDatastoreEntity:
        return await self.run_in_executor(functools.partial(client.put, entity)) # type: ignore

    async def persist(
        self,
        object: ResourceType,
        transaction: ITransaction | None = None,
        model: type[ResourceType] | None = None,
        **kwargs: Any
    ) -> ResourceType:
        entity = self.entity_factory(self.resource_key(object, model=model), object)
        await self.persist_entity(transaction or self.client, entity)
        return object