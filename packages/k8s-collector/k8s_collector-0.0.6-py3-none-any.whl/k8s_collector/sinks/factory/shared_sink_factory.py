from k8s_collector.config.models.sinks import SinkConfig
from k8s_collector.sinks import Sink
from k8s_collector.sinks.factory.basic_sink_factory import BasicSinkFactory
from k8s_collector.sinks.factory.sink_factory import SinkFactory


class SharedSinkFactory(SinkFactory):
    """
    cache the given sink factory or BasicSinkFactory if not provided with id(Resource) as cache key
    """

    def __init__(self, sink_factory: SinkFactory | None = None):
        self._sink_factory: SinkFactory = sink_factory or BasicSinkFactory()
        self._shared_sinks: list[tuple[SinkConfig, Sink]] = []

    def get_sink(self, sink_config: SinkConfig) -> Sink:
        for shared_sink_config, shared_sink in self._shared_sinks:
            if sink_config == shared_sink_config:
                return shared_sink

        sink: Sink = self._sink_factory.get_sink(sink_config)
        self._shared_sinks.append((sink_config, sink))
        return sink
