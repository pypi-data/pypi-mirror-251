# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic

from ..objectmeta import ObjectMeta
from .base import BaseNamespace
from .namespacespec import NamespaceSpec


class OrganizationSpec(NamespaceSpec):
    model_config = {'populate_by_name': True}

    id: int | None = pydantic.Field(
        default=None,
        title="Organization ID",
        description=(
            "A numeric identifier for this organization. This field is "
            "auto-generated and can not be set or changed."
        ),
        frozen=True
    )

    display_name: str = pydantic.Field(
        default=...,
        alias='displayName',
        description=(
            "The display name of the `Organization` for user "
            "interfaces."
        )
    )


class Organization(BaseNamespace[ObjectMeta[str]], kind='Namespace', type='webiam.io/organization'):
    model_config = {'populate_by_name': True}

    spec: 'OrganizationSpec' = pydantic.Field(
        default=...,
        description="Defines the behavior of the `Namespace`."
    )