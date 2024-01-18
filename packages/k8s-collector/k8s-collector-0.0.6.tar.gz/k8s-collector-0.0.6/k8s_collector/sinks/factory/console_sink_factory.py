from k8s_collector.config.models.sinks import SinkConfig
from k8s_collector.sinks import Sink
from k8s_collector.sinks.console import ConsoleSink
from k8s_collector.sinks.console.console_formatter import ConsoleFormatter
from k8s_collector.sinks.factory import SinkFactory


class ConsoleSinkFactory(SinkFactory):
    def get_sink(self, sink_config: SinkConfig) -> Sink:
        self._raise_for_type(sink_config, expected_type='console')
        # it's probably safe to assume the SinkConfig type is already validated and parsed to the specific type
        console_formatter: ConsoleFormatter = ConsoleFormatter(sink_config.format)
        return ConsoleSink(console_formatter)
