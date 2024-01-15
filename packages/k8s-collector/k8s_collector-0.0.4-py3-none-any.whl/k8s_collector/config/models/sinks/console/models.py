from dataclasses import dataclass

from k8s_collector.config.models.sinks.models import SinkConfig


@dataclass(frozen=True)
class ConsoleSinkConfig(SinkConfig):
    format: str | None
