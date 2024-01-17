# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import copy
import inspect
import logging
from collections import OrderedDict
from typing import cast
from typing import Any
from typing import Callable
from typing import Generic
from typing import NoReturn
from typing import TypeVar

import fastapi
import pydantic
from fastapi.exceptions import HTTPException

from canonical.exceptions import Duplicate
from canonical.exceptions import Immutable
from canonical.exceptions import ReferentDoesNotExist
from canonical.ext.resource import Error
from canonical.ext.resource import ResourceType
from canonical.ext.resource import IResourceRepository
from canonical.ext.iam.protocols import IResourceAuthorizationContext
from canonical.utils import throw
from ..params import AcceptedContentType
from ..params import RequestAuthorizationContext
from ..params import RequestResourceName
from ..params import RequestVerb
from ..params import ResourceRepository
from ..response import Response
from ..utils import inject
from .basemetaclass import BaseMetaclass
from .endpoint import Endpoint
from .validator import Validator


T = TypeVar('T')


class BaseOperation(Generic[T], metaclass=BaseMetaclass):
    creates: bool = False
    dependants: list[Callable[..., Any]]
    dependencies: list[Any]
    description: str | None = None
    handle: Any
    input_model: type[pydantic.BaseModel] | None = None
    input_params: set[str]
    logger: logging.Logger = logging.getLogger('uvicorn')
    method: str
    model: type[ResourceType]
    path: str | None = None
    permissions: set[str]
    summary: str | None = None
    verb: str = ''

    default_responses: dict[int, Any] = {
        401: {
            'model': Error,
            'description': (
                "Authentication is required to perform the requested "
                "operation or the provided credential is invalid."
            )
        },
        403: {
            'model': Error,
            'description': (
                "Untrusted credential or the authenticated request is not allowed "
                "to perform the requested operation."
            )
        },
        406: {
            'model': Error,
            'description': (
                "The media type accepted by the client can not be "
                "satisfied by the server."
            )
        },
        500: {
            'model': Error,
            'description': (
                "The server encountered an unexpected condition that "
                "prevented it from fulfilling the request."
            )
        }
    }
    detail: bool = False
    existing: bool = False
    requires_body: bool = False
    status_code: int = 200

    def __init__(
        self,
        *,
        model: type[ResourceType],
        verb: str | None = None,
        method: str | None = None,
        path: str | None = None,
        permissions: set[str] | None = None,
        summary: str | None = None,
        description: str | None = None,
        validator: type[Validator[Any]] = Validator,
        context_class: type[IResourceAuthorizationContext] | None = None,
    ) -> None:
        self.context_class = context_class
        self.description = description
        self.input_params = set()
        self.method = method or self.method
        self.model = model
        self.path = path
        self.summary = summary
        self.validator_class = validator
        if verb is not None:
            self.verb = verb
        if not self.verb:
            raise TypeError(
                f"{type(self).__name__}.__init__() missing 1 required "
                "positional argument: 'verb'"
            )
        self.dependants = []
        self.dependencies = [
            fastapi.Depends(self.context_class or (lambda: None)),
            fastapi.Depends(self.inject_verb(self.verb)),
            fastapi.Depends(self.inject_model),
        ]
        self.permissions = set(permissions or [])
        if self.is_namespaced():
            self.dependencies.append(fastapi.Depends(self.inject_namespace))
        if self.is_detail():
            self.dependencies.append(fastapi.Depends(self.inject_name))
        if self.needs_existing():
            self.dependencies.append(fastapi.Depends(self.inject_existing))
        if self.input_model is not None:
            self.requires_body = True
        if self.requires_body:
            self.dependencies.extend([
                AcceptedContentType({'application/yaml', 'application/json'}),
                fastapi.Depends(self.inject_validator())
            ])

    def add_to_router(
        self,
        router: fastapi.FastAPI | fastapi.APIRouter,
        register: Callable[[type[ResourceType], str], None],
        authorization: type[IResourceAuthorizationContext] | None = None
    ):
        if authorization:
            self.dependencies = [
                *inject(resource_context=authorization),
                *self.dependencies
            ]
        router.add_api_route(
            methods=[self.method],
            path=self.get_path(),
            endpoint=self.as_handler(),
            name=self.get_endpoint_name(),
            summary=self.get_endpoint_summary(),
            description=getattr(self.handle, '__doc__', None),
            dependencies=[*self.dependencies, fastapi.Depends(self.authorize)],
            responses={**self.get_openapi_responses()},
            response_description=self.get_response_description(),
            response_model=self.get_response_model(),
            response_model_by_alias=True,
            status_code=self.status_code,
            tags=[self.model.__name__],
            operation_id=self.get_endpoint_name()
        )
        register(self.model, self.verb)

    def annotate_handler(
        self,
        signature: inspect.Signature
    ) -> inspect.Signature:
        return signature

    def as_handler(self):
        # Do some modifications on the signatures because for
        # the base implementation classes, not every type is
        # known yet (i.e. the actual model).
        try:
            sig = inspect.signature(self.handle)
        except ValueError:
            raise TypeError(
                "Invalid signature for handler function or method. "
                f"Does {self.handle.__module__}.{self.handle.__name__}() "
                "take a verb.Verb instance as its first positional "
                "argument?"
            )
        params: OrderedDict[str, inspect.Parameter] = OrderedDict(sig.parameters)
        for param in sig.parameters.values():
            if param.annotation != ResourceType:
                continue
            params[param.name] = param.replace(annotation=self.get_model())

        if not params.get('request'):
            params['request'] = inspect.Parameter(
                kind=inspect.Parameter.POSITIONAL_ONLY,
                name='request',
                annotation=fastapi.Request
            )

        sig = sig.replace(
            parameters=list(sorted(params.values(), key=lambda x: x.kind))
        )
        return Endpoint(
            name=self.get_endpoint_name(),
            signature=self.annotate_handler(sig),
            handle=self,
        )

    def depends(self, func: Callable[..., Any]) -> Callable[..., Any]:
        self.dependants.append(func)
        return func

    def fail(self, status_code: int, detail: str) -> NoReturn:
        raise HTTPException(status_code=status_code, detail=detail)

    def get_endpoint_name(self) -> str:
        return f'{self.model.plural}.{self.verb}'

    def get_endpoint_summary(self) -> str:
        return self.summary or throw(NotImplementedError)

    def get_input_model(self) -> type[pydantic.BaseModel]:
        return self.model.InputModel

    def get_model(self) -> type[pydantic.BaseModel]:
        return self.model

    def get_openapi_responses(self) -> dict[int, dict[str, Any]]:
        responses = copy.deepcopy(self.default_responses)
        if self.detail:
            responses[404] = {
                'model': Error,
                'description': (
                    f'The {self.model.__name__} specified by the path parameter(s) '
                    'does not exist.'
                )
            }
        if self.requires_body:
            responses[415] = {
                'model': Error,
                'description': "Invalid content type for request body."
            }
        if self.method == 'HEAD':
            responses.pop(406)
        return responses

    def get_path(self) -> str:
        path = f'{self.model.base_path}'
        if self.detail:
            path = f'{path}/{{name}}'
        path = f'/{path}'
        if self.path:
            assert not str.startswith(self.path, '/')
            path = f'{path}{self.path}'
        return path

    def get_response_description(self) -> str:
        return self.description or throw(NotImplementedError)

    def get_response_model(self) -> type[pydantic.BaseModel] | None:
        if self.method == 'HEAD':
            return None
        return self.model if (self.detail or self.creates) else self.model.List

    def inject_name(
        self,
        request: fastapi.Request,
        name: str = fastapi.Path(
            description=f'The `.metadata.name` of an existing resource.',
            max_length=64,
        )
    ):
        setattr(request.state, 'name', name)

    def inject_namespace(
        self,
        request: fastapi.Request,
        namespace: str = fastapi.Path(
            description=(
                "Identifies the namespace that contains the "
                "resource."
            )
        ),
    ):
        setattr(request.state, 'namespace', namespace)

    def inject_model(self, request: fastapi.Request):
        setattr(request.state, 'model', self.model)

    def inject_validator(self):
        def f(request: fastapi.Request, validator: Validator[Any] = fastapi.Depends(self.validator_class)):
            setattr(request.state, 'validator', validator)
        return f

    def inject_verb(self, verb: str):
        def f(request: fastapi.Request):
            setattr(request.state, 'verb', verb)
        return f

    def is_detail(self) -> bool:
        return self.detail

    def is_namespaced(self) -> bool:
        return self.model.is_namespaced()

    def needs_existing(self) -> bool:
        return self.existing

    def on_not_authenticated(self):
        raise HTTPException(
            status_code=401,
            detail="Authentication required."
        )

    def on_unauthorized(self):
        raise HTTPException(
            status_code=403,
            detail=(
                "The request subject is not granted permission "
                "to perform this operation."
            )
        )

    def replaces(self) -> bool:
        return False

    async def authorize(
        self,
        ctx: RequestAuthorizationContext,
        verb: RequestVerb
    ) -> None:
        if verb == 'authorize':
            return
        if not ctx.is_authenticated():
            self.on_not_authenticated()
        if not ctx.is_authorized():
            self.on_unauthorized()

        if self.permissions and not await ctx.has(self.permissions):
            raise NotImplementedError

    async def inject_existing(
        self,
        request: fastapi.Request,
        ctx: RequestAuthorizationContext,
        resources: ResourceRepository,
        key: RequestResourceName
    ) -> None:
        try:
            obj = await resources.get(key)
            assert obj is not None
        except resources.DoesNotExist:
            self.fail(404, f"{self.model.__name__} does not exist.")
        await self.on_mutation_request(request, ctx, resources, cast(T, obj))
        setattr(request.state, 'resource', obj)

    async def model_factory(
        self,
        request: fastapi.Request,
        repo: ResourceRepository,
        obj: Any
    ) -> Any:
        if not isinstance(obj, self.model.InputModel):
            raise TypeError(
                f"Can not create a new {self.model.__name__} from "
                f"{type(obj).__name__}"
            )
        # Parse directly from the request JSON content because some
        # fields may be excluded if we would use model_dump().
        return self.model.model_validate(await request.json())

    async def on_mutation_request(
        self,
        request: fastapi.Request,
        ctx: IResourceAuthorizationContext,
        repo: IResourceRepository[Any],
        resource: T
    ) -> None:
        """Hook to implement logic prior to mutating a resource."""
        pass

    async def render_to_response(self, result: T) -> fastapi.Response:
        if isinstance(result, pydantic.BaseModel):
            result = Response( # type: ignore
                status_code=self.status_code,
                content=result
            )
        if not isinstance(result, fastapi.Response):
            raise NotImplementedError
        return result

    async def __call__(
        self,
        request: fastapi.Request,
        *args: Any, **kwargs: Any
    ) -> fastapi.Response:
        validator: Validator[Any] | None = getattr(request.state, 'validator', None)
        repo: ResourceRepository = getattr(request.state, 'resources')
        sig = inspect.signature(self.handle)
        if sig.parameters.get('request'):
            kwargs['request'] = request
        params: dict[str, Any] = {}
        new = None
        for name, value in kwargs.items():
            if name not in sig.parameters:
                continue
            if name in self.input_params:
                value = new = await self.model_factory(request, repo, value)
                if not validator:
                    self.logger.critical(
                        "Received input from request but no validator was "
                        "injected (url: %s)",
                        str(request.url)
                    )
            params[name] = value
        if validator is not None:
            await validator.validate(self, new)
        try:
            result = await self.handle(**params)
        except Duplicate:
            self.fail(409, "Resource conflict.")
        except (Immutable, ReferentDoesNotExist) as e:
            self.fail(409, e.detail)
        return await self.render_to_response(result)