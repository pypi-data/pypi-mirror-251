from k8s_collector.config.parsers.sinks.console_sink_config_parser import ConsoleSinkConfigParser
from k8s_collector.config.parsers.sinks.factory.sink_config_parser_factory import SinkConfigParserFactory
from k8s_collector.config.parsers.sinks.http_sink_config_parser import HttpSinkConfigParser
from k8s_collector.config.parsers.sinks.sink_config_parser import SinkConfigParser


class BasicSinkConfigParserFactory(SinkConfigParserFactory):
    def __init__(self):
        self._sink_type_to_sink_config_parser_map: dict[str, SinkConfigParser] = {
            'http': HttpSinkConfigParser(),
            'console': ConsoleSinkConfigParser()
        }

    def get_sink_config_parser(self, sink_obj: dict) -> SinkConfigParser:
        sink_type: str = sink_obj['type']
        return self._sink_type_to_sink_config_parser_map[sink_type]
