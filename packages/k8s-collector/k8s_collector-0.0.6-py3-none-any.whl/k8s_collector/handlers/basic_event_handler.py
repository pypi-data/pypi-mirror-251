import traceback
from typing import Callable

from k8s_collector.config.models import Resource
from k8s_collector.filterers import EventFilterer
from k8s_collector.handlers.event_handler import EventHandler
from k8s_collector.processors import EventProcessor
from k8s_collector.sinks import Sink
from k8s_collector.sinks.factory import SinkFactory


class BasicEventHandler(EventHandler):
    def __init__(self, event_filterer: EventFilterer, event_processor: EventProcessor, sink_factory: SinkFactory):
        self._event_filterer: EventFilterer = event_filterer
        self._event_processor: EventProcessor = event_processor
        self._sink_factory = sink_factory
        self._event_type_to_handler_map: dict[str, Callable[[list[Sink], dict], None]] = {
            "ADDED": self._handle_added,
            "MODIFIED": self._handle_modified,
            "DELETED": self._handle_deleted,
        }

    def handle(self, event: dict, resource: Resource) -> None:
        event_type: str = event['type']
        print(f'got event type: {event_type}')
        try:
            filtered_event: dict | None = self._event_filterer.filter(event, resource)
            if not filtered_event:
                print(f'filter out event')
                return
            processed_event: dict = self._event_processor.process(filtered_event, resource)
            sinks: list[Sink] = [self._sink_factory.get_sink(sink_config) for sink_config in resource.sinks]
            handler: Callable[[list[Sink], dict], None] | None = self._event_type_to_handler_map.get(event_type)
            if not handler:
                # TODO: define logging
                print(f'cannot handle event of type {event_type}, pass')
                return
            handler(sinks, processed_event)
        except Exception as err:
            print(f'error occurred while handling event, error: {err}')
            traceback.print_exc()

    def _handle_added(self, sinks: list[Sink], obj: dict) -> None:
        for sink in sinks:
            sink.add(obj)

    def _handle_modified(self, sinks: list[Sink], obj: dict) -> None:
        for sink in sinks:
            sink.update(obj)

    def _handle_deleted(self, sinks: list[Sink], obj: dict) -> None:
        for sink in sinks:
            sink.delete(obj)
