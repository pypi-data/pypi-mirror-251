# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
import logging
from typing import cast
from typing import Any
from typing import Generic
from typing import TypeVar
from typing import TYPE_CHECKING

import fastapi

from canonical.exceptions import ReferentDoesNotExist
from canonical.ext.resource import ResourceType
from ..params import ResourceModel
from ..params import ResourceRepository
if TYPE_CHECKING:
    from .base import BaseOperation


T = TypeVar('T')


class Validator(Generic[T]):
    """Validates the input data for verbs."""
    __module__: str = 'canonical.ext.fastapi'
    logger: logging.Logger = logging.getLogger('uvicorn')
    model: type[T]
    old: T | None
    new: T | None

    def __init__(
        self,
        request: fastapi.Request,
        repo: ResourceRepository,
        model: ResourceModel
    ):
        self.model = cast(type[T], model)
        self.namespace = getattr(request.state, 'namespace', None)
        self.new = None
        self.old = None
        self.repo = repo
        self.request = request

    def get_validator_func(self, verb: 'BaseOperation[Any]'):
        return getattr(self, f'on_{verb.verb}', None)

    async def check_references(
        self,
        repo: ResourceRepository,
        obj: T
    ) -> None:
        # TODO: Does not work
        for ref in cast(ResourceType, obj).get_references():
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

    async def validate(self, verb: 'BaseOperation[Any]', obj: T | None = None):
        """Runs the validators for the specified resource."""
        self.fail = verb.fail
        self.new = obj
        self.verb = verb
        if verb.requires_body:
            if self.new is None:
                verb.fail(422, "Input required.")
            self.old = await self.get_object(
                obj=cast(ResourceType, obj),
                require=verb.needs_existing()
            )
            if verb.creates and self.old is not None:
                self.fail(409, "Object exists.")
            resource = cast(ResourceType, obj)
            if not resource.in_namespace(self.namespace):
                verb.fail(403,
                    "Not allowed to create this object in the namespace "
                    "defined by the path."
                )

            # Handle replace.
            if self.old and self.new:
                new = cast(ResourceType, self.new)
                old = cast(ResourceType, self.old)

                # The object must be replaceable.
                if not old.replacable() and verb.replaces():
                    self.fail(409, "Object can not be replaced")

            await self.check_references(self.repo, self.new)

        func = self.get_validator_func(verb)
        if func is None:
            self.logger.warning(
                "%s does not define a validation handler for verb '%s'.",
                type(self).__name__,
                verb.verb
            )
            return
        result = func(new=self.new, old=self.old)
        if inspect.isawaitable(result):
            await result

    async def get_object(
        self,
        obj: ResourceType,
        require: bool = False
    ) -> T | None:
        """Return the existing version of an object."""
        try:
            return await self.repo.get(obj.key) # type: ignore
        except self.repo.DoesNotExist:
            if require:
                self.fail(404, "The object does not exist.")
            return None