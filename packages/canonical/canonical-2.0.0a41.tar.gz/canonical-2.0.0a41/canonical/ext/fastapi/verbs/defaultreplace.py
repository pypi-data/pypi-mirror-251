# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import TypeVar

from canonical.ext.resource import ResourceType
from .replace import Replace
from ..params import ResourceRepository


T = TypeVar('T', bound=ResourceType)


class DefaultReplace(Replace[T]):
    creates = False
    detail = True
    exists = True
    method = 'PUT'
    requires_body = True
    status_code = 205
    verb = 'replace'

    async def handle(
        self,
        repo: ResourceRepository,
        obj: ResourceType
    ) -> ResourceType:
        return await obj.persist(repo, mode='replace')