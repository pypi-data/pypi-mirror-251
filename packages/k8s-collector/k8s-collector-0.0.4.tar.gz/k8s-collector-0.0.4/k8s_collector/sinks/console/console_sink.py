from k8s_collector.sinks.console.console_formatter import ConsoleFormatter
from k8s_collector.sinks.sink import Sink


class ConsoleSink(Sink):
    def __init__(self, console_formatter: ConsoleFormatter):
        self._console_formatter: ConsoleFormatter = console_formatter

    def add(self, obj: dict) -> None:
        formatted_obj: str = self._console_formatter.add(obj)
        print(formatted_obj)

    def update(self, obj: dict) -> None:
        formatted_obj: str = self._console_formatter.update(obj)
        print(formatted_obj)

    def delete(self, obj: dict) -> None:
        formatted_obj: str = self._console_formatter.delete(obj)
        print(formatted_obj)
