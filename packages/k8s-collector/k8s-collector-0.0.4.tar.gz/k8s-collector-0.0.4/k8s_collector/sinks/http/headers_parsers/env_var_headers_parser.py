import os

from k8s_collector.sinks.http.headers_parsers.headers_parser import HttpSinkHeadersParser


class EnvVarHttpSinkHeadersParser(HttpSinkHeadersParser):
    def __init__(self):
        self._env_vars_map: dict[str, str] = {f'env__{k}': v for k, v in os.environ.items()}

    def parse_headers(self, headers: dict[str, str] | None) -> dict[str, str] | None:
        if not headers:
            return None

        return {
            header_key: header_value.format(**self._env_vars_map)
            for header_key, header_value
            in headers.items()
        }
