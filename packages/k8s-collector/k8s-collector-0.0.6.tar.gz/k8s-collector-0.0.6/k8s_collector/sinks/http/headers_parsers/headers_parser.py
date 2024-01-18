import abc


class HttpSinkHeadersParser(abc.ABC):
    @abc.abstractmethod
    def parse_headers(self, headers: dict[str, str] | None) -> dict[str, str] | None:
        raise NotImplementedError
