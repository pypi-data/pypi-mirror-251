# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
from typing import cast
from typing import get_args
from typing import Any
from typing import Generic
from typing import Self
from typing import TypeVar
from typing import TYPE_CHECKING

import pydantic

from .condition import Condition
from .conditiontype import ConditionType
if TYPE_CHECKING:
    from .statefulresource import StatefulResource

C = TypeVar('C', bound=ConditionType[Any])


class ResourceStatus(pydantic.BaseModel, Generic[C]):
    _adapter: pydantic.TypeAdapter[C]
    _dirty: bool = pydantic.PrivateAttr(
        default=False,
    )

    changed: datetime.datetime = pydantic.Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        description=(
            "The date and time of the last change to this {kind}."
        )
    )

    version: int = pydantic.Field(
        default=...,
        description=(
            "Current version of the {kind}."
        )
    )

    message: str = pydantic.Field(
        default=...,
        description="The message of the last known condition."
    )

    current: str = pydantic.Field(
        default=...,
        description="The status of the last known condition."
    )

    conditions: list[Condition[C, Self]] = pydantic.Field(
        default_factory=list,
        description=(
            "Conditions describe specific events related to this {kind}."
        ),
        exclude=True
    )

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        ConditionImpl = cast(
            Condition[Any, Any],
            cls.model_fields['conditions'].annotation
        )
        model, *_ = get_args(ConditionImpl)
        cls._adapter = pydantic.TypeAdapter(model)

    @classmethod
    def contribute_to_class(cls, model: type['StatefulResource[Any, Any]']) -> None:
        for field in cls.model_fields.values():
            if field.description is None:
                continue
            field.description = str.format(field.description, kind=model.__name__)
        assert cls.model_rebuild(force=True)