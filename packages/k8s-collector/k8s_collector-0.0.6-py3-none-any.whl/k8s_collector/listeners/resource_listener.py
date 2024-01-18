import abc
from typing import NoReturn

from k8s_collector.config.models import AggregatedResource


class ResourceListener(abc.ABC):
    @abc.abstractmethod
    def listen(self, aggregated_resource: AggregatedResource, namespace: str | None) -> NoReturn:
        raise NotImplementedError


class MultiResourceListener(abc.ABC):
    @abc.abstractmethod
    def listen(self, aggregated_resources: list[AggregatedResource], namespace: str | None) -> NoReturn:
        raise NotImplementedError
