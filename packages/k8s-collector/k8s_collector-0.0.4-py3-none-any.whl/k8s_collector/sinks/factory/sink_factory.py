import abc

from k8s_collector.config.models.sinks import SinkConfig
from k8s_collector.sinks import Sink


class SinkFactory(abc.ABC):
    @abc.abstractmethod
    def get_sink(self, sink_config: SinkConfig) -> Sink:
        raise NotImplementedError

    def _raise_for_type(self, sink_config: SinkConfig, expected_type: str) -> None:
        if sink_config.type != expected_type:
            raise ValueError(f'for {expected_type} sink use "type: {expected_type}", given type: {sink_config.type}')
