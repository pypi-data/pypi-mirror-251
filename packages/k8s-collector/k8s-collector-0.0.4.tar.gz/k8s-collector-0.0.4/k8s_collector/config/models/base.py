from dataclasses import dataclass
from typing import Any

from k8s_collector.config.models.sinks.models import SinkConfig


@dataclass(frozen=True)
class EntityMapping:
    identifier: str
    title: str
    blueprint: str
    team: str
    properties: dict[str, Any]
    relations: dict[str, str] | None


@dataclass(frozen=True)
class Entity:
    mappings: list[EntityMapping]


@dataclass(frozen=True)
class Selector:
    query: str


@dataclass(frozen=True)
class Resource:
    api_version: str
    kind: str
    selector: Selector
    entity: Entity
    sinks: list[SinkConfig]


@dataclass(frozen=True)
class CollectorConfig:
    resources: list[Resource]


@dataclass(frozen=True)
class AggregatedResource:
    api_version: str
    kind: str
    resources: list[Resource]
