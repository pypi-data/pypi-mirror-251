from k8s_collector.sinks.http.client import HttpClient
from k8s_collector.sinks.sink import Sink


class HttpSink(Sink):
    def __init__(self, http_client: HttpClient):
        self._http_client = http_client

    def add(self, obj: dict) -> None:
        self._http_client.add(obj)

    def update(self, obj: dict) -> None:
        self._http_client.update(obj)

    def delete(self, obj: dict) -> None:
        self._http_client.delete(obj)