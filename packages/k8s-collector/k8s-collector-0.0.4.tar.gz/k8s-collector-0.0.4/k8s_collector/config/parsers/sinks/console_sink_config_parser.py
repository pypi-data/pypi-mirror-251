from k8s_collector.config.models.sinks import SinkConfig
from k8s_collector.config.models.sinks.console import ConsoleSinkConfig
from k8s_collector.config.parsers.exceptions import ParseError
from k8s_collector.config.parsers.sinks.sink_config_parser import SinkConfigParser


class ConsoleSinkConfigParser(SinkConfigParser):
    def parse(self, sink_obj: dict) -> SinkConfig:
        try:
            sink_type: str = sink_obj['type']
            format: str | None = sink_obj.get('format')
            return ConsoleSinkConfig(type=sink_type, format=format)
        except KeyError as err:
            raise ParseError(f"Couldn't find {err} in console sink config")
