from k8s_collector.config.models.sinks import SinkConfig
from k8s_collector.config.models.sinks.http import HttpSinkConfig
from k8s_collector.sinks import Sink
from k8s_collector.sinks.factory import SinkFactory
from k8s_collector.sinks.http import HttpSink
from k8s_collector.sinks.http.client import HttpClient
from k8s_collector.sinks.http.headers_parsers.env_var_headers_parser import EnvVarHttpSinkHeadersParser


class HttpSinkFactory(SinkFactory):
    def get_sink(self, sink_config: SinkConfig) -> Sink:
        self._raise_for_type(sink_config, expected_type='http')
        # it's probably safe to assume the SinkConfig type is already validated and parsed to the specific type
        http_client: HttpClient = self._create_http_client(sink_config)
        return HttpSink(http_client)

    def _create_http_client(self, sink_config: HttpSinkConfig) -> HttpClient:
        headers: dict[str, str] | None = self._convert_header_configs_to_headers(sink_config)
        return HttpClient(url=sink_config.url, headers=headers, headers_parser=EnvVarHttpSinkHeadersParser())

    def _convert_header_configs_to_headers(self, sink_config: HttpSinkConfig) -> dict[str, str] | None:
        if not sink_config.headers:
            return None

        return {header_config.key: header_config.value for header_config in sink_config.headers}
