# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import TypeVar

from canonical.exceptions import ReferentDoesNotExist
from canonical.ext.resource import ResourceType
from .create import Create
from ..params import ResourceRepository


T = TypeVar('T', bound=ResourceType)


class DefaultCreate(Create[T]):
    creates = True
    detail = False
    exists = False
    method = 'POST'
    requires_body = True
    status_code = 201
    verb = 'create'

    async def check_references(
        self,
        repo: ResourceRepository,
        obj: ResourceType
    ) -> None:
        for ref in obj.get_references():
            if not ref.is_local() or ref.is_namespaced():
                raise NotImplementedError
            if await repo.exists(ref):
                self.logger.info(
                    "Reference exists (apiGroup: %s, kind: %s, name: %s)",
                    ref.api_group, ref.kind, ref.name
                )
                continue
            raise ReferentDoesNotExist(
                f"Reference {ref.name} does not exist (kind: {ref.kind})"
            )

    async def handle(
        self,
        repo: ResourceRepository,
        obj: ResourceType
    ) -> ResourceType:
        await self.check_references(repo, obj)
        return await obj.persist(repo)