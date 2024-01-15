import abc

from k8s_collector.config.models.sinks.models import SinkConfig


class SinkConfigParser(abc.ABC):
    """
    IMPORTANT: SinkConfigParser implementation should parse the generic SinkConfig to specific SinkConfig
    and MUST NOT parse sensitive data as it might be sent over the network, it should be injected to the specific client
    """
    @abc.abstractmethod
    def parse(self, sink_obj: dict) -> SinkConfig:
        raise NotImplementedError
