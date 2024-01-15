class ConsoleFormatter:
    def __init__(self, format: str | None = None):
        self._format: str = format

    def add(self, obj: dict) -> str:
        return self._do_format(obj=obj, event_type='ADDED')

    def update(self, obj: dict) -> str:
        return self._do_format(obj=obj, event_type='MODIFIED')

    def delete(self, obj: dict) -> str:
        return self._do_format(obj=obj, event_type='DELETED')

    def _do_format(self, obj: dict, event_type: str) -> str:
        return self._format.format(obj=obj, event=event_type) if self._format else repr(obj)
