from __future__ import annotations

from typing import List, Literal
from pydantic import BaseModel

type BucketSubscriptionScope = Literal["create"] | Literal["delete"]

type BucketIntegrationScope = (
    Literal["get"] | Literal["list"] | Literal["put"] | Literal["delete"]
)

type ResourceType = Literal["bucket"] | Literal["queue"] | Literal["function"]

type DependencyGroup = NonEmptyList[str] | str | None

type NonEmptyList[Item] = list[Item]


class BindingSpec(BaseModel):
    resource_type: ResourceType
    resource_id: str
    scopes: list[str]
    props: dict[str, str] | None


class BucketBindingSpec(BindingSpec):
    selector: str | None


class PythonPoetryArgs(BaseModel):
    with_: DependencyGroup | None = None
    without: DependencyGroup | None = None
    dev: bool | None = None
    all_extras: bool | None = None
    without_hashes: bool | None = None
    without_urls: bool | None = None


# defines the bindings within a Python module (file)
class ModuleSpec(PythonPoetryArgs):
    file_name: str
    bindings: list[BindingSpec] | None


class FunctionSpec(PythonPoetryArgs):
    function_id: str
    file_name: str
    bindings: list[BindingSpec] | None


class BucketSubscriptionSpec(BaseModel):
    scopes: List[BucketSubscriptionScope]
    function_id: str


class BucketSpec(BaseModel):
    bucket_id: str
    subscriptions: list[BucketSubscriptionSpec]


class QueueSubscriptionSpec(BaseModel):
    function_id: str


class QueueSpec(BaseModel):
    queue_id: str
    fifo: bool
    subscriptions: list[QueueSubscriptionSpec]


class PackyakSpec(BaseModel):
    modules: list[ModuleSpec]
    buckets: list[BucketSpec]
    queues: list[QueueSpec]
    functions: list[FunctionSpec]
