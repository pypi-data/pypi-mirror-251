# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Annotated

from canonical.lib.protocols import ICache
from ..utils import request_state as s


__all__: list[str] = [
    'DefaultCache'
]


DefaultCache = Annotated[ICache, s('cache', ICache, True)]