# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import inspect
from typing import cast
from typing import get_args
from typing import Any
from typing import ClassVar
from typing import Generic
from typing import Self
from typing import TypeVar
from typing import Union
from typing import TYPE_CHECKING

import pydantic

from .condition import Condition
from .conditiontype import ConditionType
from .objectmeta import ObjectMeta
if TYPE_CHECKING:
    from .statefulresource import StatefulResource

C = TypeVar('C', bound=ConditionType[Any])


class ResourceStatus(pydantic.BaseModel, Generic[C]):
    __abstract__: ClassVar[bool] = True
    StorageModel: ClassVar[type[Condition[Any, Self]]]
    _adapter: ClassVar[pydantic.TypeAdapter[Any]]
    _resource: 'StatefulResource[Any, Any]' = pydantic.PrivateAttr(
        default=None
    )
    _dirty: bool = pydantic.PrivateAttr(
        default=False,
    )

    changed: datetime.datetime = pydantic.Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        description=(
            "The date and time of the last change to this {kind}."
        )
    )

    dirty: bool = pydantic.Field(
        default=False,
        exclude=True
    )

    version: int = pydantic.Field(
        default=0,
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
    )

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        if cls.__abstract__:
            cls.__abstract__ = False
            return
        ConditionImpl = cast(
            Condition[Any, Any],
            cls.model_fields['conditions'].annotation
        )
        model, *_ = get_args(ConditionImpl)
        cls._adapter = pydantic.TypeAdapter(model)

        # Create a model for the conditions that includes
        # the UID of the Resource. This allows persistencee
        # in a different storage container (e.g. table).
        if hasattr(cls, 'StorageModel'):
            return
        root = model.model_fields['root'].annotation
        types = list(get_args(root))
        if not types:
            # Base class, nothing to do.
            return
        
        # Check if all classes inherit from ConditionType.
        for i, t in enumerate(types):
            if not inspect.isclass(t)\
            or not issubclass(t, ConditionType):
                raise TypeError("Must inherit from ConditionType.")
            types[i] = t.StorageModel
        cls.StorageModel = type(
            f'{cls.__name__}Condition',
            (pydantic.RootModel,),
            {
                '__annotations__': {
                    'root': Union[*types] # type: ignore
                }
            }
        )

    @classmethod
    def contribute_to_class(cls, model: type['StatefulResource[Any, Any]']) -> None:
        for field in cls.model_fields.values():
            if field.description is None:
                continue
            field.description = str.format(field.description, kind=model.__name__)
        assert cls.model_rebuild(force=True)

    @property
    def adapter(self) -> pydantic.TypeAdapter[Condition[C, Self]]:
        return self._adapter

    @property
    def resource(self) -> 'StatefulResource[ObjectMeta[Any], Any]':
        return self._resource

    def apply(self, status: str, **kwargs: Any):
        kwargs.setdefault('timestamp', datetime.datetime.now(datetime.timezone.utc))
        condition = self.adapter.validate_python({
            'status': status,
            'observed_generation': self.resource.metadata.generation,
            **kwargs
        })
        self._apply(condition)

    def attach(self, resource: 'StatefulResource[Any, Any]'):
        self._resource = resource

    def is_dirty(self) -> bool:
        return self.dirty

    def is_final(self):
        return self.resource.is_final()

    def storage_model(self, data: Any) -> Condition[C, Self]:
        return self.StorageModel.model_validate(data)

    def _apply(
        self,
        condition: Condition[C, Self],
        replay: bool = False
    ) -> Condition[C, Self]:
        if self.is_final() and not replay:
            raise ValueError("Resource is in its final state.")
        if condition.timestamp == self.changed:
            condition.timestamp += datetime.timedelta(microseconds=1)
        self.changed = condition.timestamp
        self.message = condition.message
        self.current = condition.status
        condition.apply(self)
        if not replay:
            self.conditions.append(condition)
        if not replay:
            self.dirty = True
        return condition