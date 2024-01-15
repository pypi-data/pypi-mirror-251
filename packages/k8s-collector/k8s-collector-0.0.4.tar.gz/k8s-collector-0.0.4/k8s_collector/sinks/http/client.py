import httpx

from k8s_collector.sinks.http.headers_parsers.headers_parser import HttpSinkHeadersParser


class HttpClient:
    def __init__(self, url: str, headers: dict[str, str] | None, headers_parser: HttpSinkHeadersParser):
        # not closing the connection because k8s-collector suppose to run indefinitely
        # and potentially a lot of resources will be changed frequently in heavy-loaded cluster
        self._headers_parser: HttpSinkHeadersParser = headers_parser
        self._url: str = url
        self._preparsed_headers: dict[str, str] | None = headers
        self._parsed_headers: dict[str, str] | None = self._headers_parser.parse_headers(headers)
        self._client = httpx.Client(headers=self._parsed_headers)

    def add(self, obj: dict) -> None:
        try:
            self._client.post(self._url, json=obj)
        except httpx.HTTPError as e:
            print(f'failed to add obj, error: {e}')

    def update(self, obj: dict) -> None:
        try:
            self._client.put(self._url, json=obj)
        except httpx.HTTPError as e:
            print(f'failed to update obj, error: {e}')

    def delete(self, obj: dict) -> None:
        # using request because delete doesn't support body, the receiver must not ignore body on delete
        try:
            self._client.request("DELETE", self._url, json=obj)
        except httpx.HTTPError as e:
            print(f'failed to delete obj, error: {e}')
