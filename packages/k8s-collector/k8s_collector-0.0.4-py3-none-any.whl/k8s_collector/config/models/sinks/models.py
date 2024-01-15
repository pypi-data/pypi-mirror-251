from dataclasses import dataclass


@dataclass(frozen=True)
class SinkConfig:
    type: str
