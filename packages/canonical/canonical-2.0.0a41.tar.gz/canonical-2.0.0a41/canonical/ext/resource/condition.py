# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from __future__ import annotations
import datetime
from typing import get_args
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import Literal
from typing import TypeVar
from typing import TYPE_CHECKING

import pydantic

from .conditiontype import ConditionType
if TYPE_CHECKING:
    from .resourcestatus import ResourceStatus


C = TypeVar('C', bound=ConditionType[Any])
S = TypeVar('S')


class Condition(pydantic.RootModel[C], Generic[C, S]):
    status_types: ClassVar[set[str]]

    @property
    def message(self):
        return self.root.message

    @property
    def status(self):
        return self.root.status

    @property
    def timestamp(self):
        return self.root.timestamp

    @timestamp.setter
    def timestamp(self, value: datetime.datetime) -> None:
        self.root.timestamp = value

    @property
    def uid(self):
        return self.root._uid # type: ignore

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        args: tuple[C, ...] = get_args(cls.model_fields['root'].annotation)
        if not args:
            return

        cls.status_types = set()
        for model in args:
            model.contribute_to_class(cls)

    @classmethod
    def contribute_to_class(cls, model: type['ResourceStatus[Any]']):
        if not cls.status_types:
            return
        model.model_fields['current'].annotation = Literal[*cls.status_types] # type: ignore
        assert cls.model_rebuild(force=True)

    @classmethod
    def register_condition(cls, name: str):
        cls.status_types.add(name)

    def apply(self, state: S, replay: bool = False) -> None:
        return self.root.apply(state, replay=replay)

    def can_transition(self, state: S):
        return self.root.can_transition(state)

    def is_dirty(self):
        return self.root.is_dirty()

    def is_final(self) -> bool:
        return self.root.is_final()