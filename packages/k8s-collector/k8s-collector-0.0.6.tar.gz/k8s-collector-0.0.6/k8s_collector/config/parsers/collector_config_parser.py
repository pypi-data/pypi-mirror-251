import abc

from k8s_collector.config.models import CollectorConfig


class CollectorConfigParser(abc.ABC):

    @abc.abstractmethod
    def parse(self, obj: dict) -> CollectorConfig:
        raise NotImplementedError
