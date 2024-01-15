from dataclasses import dataclass

from k8s_collector.config.models.sinks.models import SinkConfig


@dataclass
class Header:
    key: str
    value: str


@dataclass(frozen=True)
class HttpSinkConfig(SinkConfig):
    url: str
    headers: list[Header] | None
