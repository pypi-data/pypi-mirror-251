from k8s_collector.config.models.sinks import SinkConfig
from k8s_collector.sinks import Sink
from k8s_collector.sinks.factory.console_sink_factory import ConsoleSinkFactory
from k8s_collector.sinks.factory.http_sink_factory import HttpSinkFactory
from k8s_collector.sinks.factory.sink_factory import SinkFactory


class BasicSinkFactory(SinkFactory):
    def __init__(self):
        self._sink_type_to_sink_factory_map: dict[str, SinkFactory] = {
            'http': HttpSinkFactory(),
            'console': ConsoleSinkFactory()
        }

    def get_sink(self, sink_config: SinkConfig) -> Sink:
        return self._sink_type_to_sink_factory_map[sink_config.type].get_sink(sink_config)
