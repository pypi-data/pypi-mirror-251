from k8s_collector.sinks.america.client import AmericaClient
from k8s_collector.sinks.sink import Sink


class AmericaSink(Sink):
    def __init__(self, america_client: AmericaClient):
        self._america_client = america_client

    def add(self, obj: dict) -> None:
        self._america_client.add(obj)

    def update(self, obj: dict) -> None:
        self._america_client.update(obj)

    def delete(self, obj: dict) -> None:
        self._america_client.delete(obj)
