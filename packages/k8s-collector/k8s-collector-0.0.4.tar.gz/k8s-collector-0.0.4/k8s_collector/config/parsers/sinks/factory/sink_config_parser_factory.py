import abc

from k8s_collector.config.parsers.sinks.sink_config_parser import SinkConfigParser


class SinkConfigParserFactory(abc.ABC):
    @abc.abstractmethod
    def get_sink_config_parser(self, sink_obj: dict) -> SinkConfigParser:
        raise NotImplementedError
