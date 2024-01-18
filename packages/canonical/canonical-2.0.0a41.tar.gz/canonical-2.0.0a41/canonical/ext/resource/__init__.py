# Copyright (C) 2023-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from .apidescriptor import APIDescriptor
from .apigroupversionlist import APIGroupVersionList
from .apiresourcelist import APIResource
from .apiresourcelist import APIResourceList
from .condition import Condition
from .conditiontype import ConditionType
from .error import Error
from .iresourcequery import IResourceQuery
from .iresourcerepository import IResourceRepository
from .listbase import ListBase
from .localreference import LocalReference
from .namespace import Namespace
from .namespacedobjectmeta import NamespacedObjectMeta
from .namespacedobjectreference import NamespacedObjectReference
from .objectmeta import ObjectMeta
from .objectreference import ObjectReference
from .primarykey import PrimaryKey
from .resource import M as ObjectMetaType
from .resource import Resource
from .resourceinspector import ResourceInspector
from .resourcemeta import ResourceMeta
from .resourceserverlist import ResourceServerList
from .resourcespec import ResourceSpec
from .resourcestatus import ResourceStatus
from .rootresource import ResourceType
from .rootresource import ResourceTypeVar
from .rootresource import RootResource
from .statefulresource import StatefulResource
from .transientmeta import TransientMeta


__all__: list[str] = [
    'APIDescriptor',
    'APIGroupVersionList',
    'APIResource',
    'APIResourceList',
    'Condition',
    'ConditionType',
    'Error',
    'IResourceQuery',
    'IResourceRepository',
    'ListBase',
    'LocalReference',
    'Namespace',
    'NamespacedObjectMeta',
    'NamespacedObjectReference',
    'ObjectMeta',
    'ObjectMetaType',
    'ObjectReference',
    'PrimaryKey',
    'Resource',
    'ResourceInspector',
    'ResourceMeta',
    'ResourceServerList',
    'ResourceSpec',
    'ResourceStatus',
    'ResourceType',
    'ResourceTypeVar',
    'RootResource',
    'StatefulResource',
    'TransientMeta',
]