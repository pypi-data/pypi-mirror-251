import abc

from k8s_collector.config.models import Resource


class EventHandler(abc.ABC):
    @abc.abstractmethod
    def handle(self, event: dict, resource: Resource) -> None:
        raise NotImplementedError
