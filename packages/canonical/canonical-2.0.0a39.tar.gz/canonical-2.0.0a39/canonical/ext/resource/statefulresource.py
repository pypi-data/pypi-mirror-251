# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
from typing import cast
from typing import get_args
from typing import Any
from typing import Generic
from typing import TypeVar

import pydantic

from .resource import M
from .resource import Resource
from .resourcestatus import ResourceStatus


S = TypeVar('S', bound=ResourceStatus[Any])


class StatefulResource(Resource[M], Generic[M, S]):
    status: S | None = pydantic.Field(
        default=None,
        description=(
            "The `status` field reports the current state of the resource. This "
            "value is modified by the system and can not be changed by clients. "
            "If the `.status` field is `null`, then the resource is created "
            "but no component or system has reported any state yet. Under "
            "normal circumstances, a state is set post-creation, and the "
            "absense of a state usually indicates an error."
        )
    )

    @classmethod
    def _status_model(cls) -> type[S]:
        return cast(type[S], cls.model_fields['status'].annotation)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        args = get_args(cls.model_fields['status'].annotation)
        if not args:
            return
        ResourceStatusImpl, *_ = args
        if not inspect.isclass(ResourceStatusImpl):
            return
        if not issubclass(ResourceStatusImpl, ResourceStatus):
            return
        ResourceStatus.contribute_to_class(cls)

    def initialize_status(self) -> None:
        pass

    def model_post_init(self, _: Any) -> None:
        self.initialize_status()