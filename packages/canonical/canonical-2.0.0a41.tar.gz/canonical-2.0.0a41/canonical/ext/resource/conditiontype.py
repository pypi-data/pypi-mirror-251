# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import Literal
from typing import TypeVar
from typing import TYPE_CHECKING

import pydantic

if TYPE_CHECKING:
    from .condition import Condition
    from .resourcestatus import ResourceStatus


R = TypeVar('R')
S = TypeVar('S', bound='ResourceStatus[Any]')


class ConditionType(pydantic.BaseModel, Generic[S]):
    """Describes the condition of a :class:`VersionedResource`."""
    StorageModel: ClassVar[type[pydantic.BaseModel]]
    model_config = {'populate_by_name': True}
    _uid: int | None = pydantic.PrivateAttr(default=None)

    timestamp: datetime.datetime = pydantic.Field(
        default=...,
        description=(
            "Specifies the date and time at which the condition "
            "emerged."
        )
    )

    message: str = pydantic.Field(
        default='',
        description=(
            "A human readable message indicating details about "
            "the transition. This may be an empty string."
        )
    )

    observed_generation: int = pydantic.Field(
        default=...,
        alias='observedGeneration',
        description=(
            "Represents the `.metadata.generation` that the "
            "condition was set based upon. For instance, if "
            "`.metadata.generation` is currently 12, but "
            "the `.status.conditions[x].observedGeneration` "
            "is 9, the condition is out of date with respect "
            "to the current state of the instance."
        )
    )

    status: str = pydantic.Field(
        default=...,
        description=(
            "Contains a programmatic identifier indicating the "
            "status of the condition's last transition. "
            "Producers of specific condition types may define "
            "expected values and meanings for this field, "
            "and whether the values are considered a guaranteed "
            "API. This field may not be empty."
        )
    )

    def __init_subclass__(cls, **kwargs: Any):
        return super().__init_subclass__()

    @classmethod
    def __pydantic_init_subclass__(cls, status: str | None = None, **kwargs: Any) -> None:
        if status is not None:
            cls.model_fields['status'].default = status
            cls.model_fields['status'].annotation = Literal[f'{status}']

            # TODO: Do not hardcode the identifier type.
            cls.StorageModel = type(
                cls.__name__,
                (cls,),
                {
                    '__annotations__': {
                        'name': str,
                        'namespace': str | None,
                        'parent': int,
                        'uid': int,
                    }
                }
            )
            cls.model_rebuild(force=True)

    @classmethod
    def contribute_to_class(cls, model: type['Condition[Any, Any]']) -> None:
        pass

    def apply(self, state: S, replay: bool = False) -> None:
        raise NotImplementedError

    def can_transition(self, state: S):
        return True

    def is_dirty(self):
        return self._uid is None

    def is_final(self) -> bool:
        return False