# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import NotRequired
from typing import TypedDict

from .base import BaseOperation as Verb
from .create import Create
from .defaultcreate import DefaultCreate
from .exists import Exists
from .get import Get
from .replace import Replace
from .retrieve import Retrieve


__all__: list[str] = [
    'Create',
    'DefaultCreate',
    'Exists',
    'Get',
    'Replace',
    'Retrieve',
    'Verb'
]


class VerbParameters(TypedDict):
    description: NotRequired[str]
    method: NotRequired[str]
    path: NotRequired[str]
    permissions: NotRequired[set[str]]
    summary: NotRequired[str]