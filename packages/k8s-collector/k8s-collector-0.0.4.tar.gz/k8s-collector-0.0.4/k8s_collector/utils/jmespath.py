import jmespath
from jmespath.parser import ParsedResult


class JmesPathQueryCache:
    def __init__(self):
        self._query_to_compiled_query_cache: dict[str, ParsedResult] = {}

    def get_or_set(self, query: str) -> ParsedResult:
        compiled_query: ParsedResult | None = self._query_to_compiled_query_cache.get(query)
        if not compiled_query:
            compiled_query = jmespath.compile(query)
            self._query_to_compiled_query_cache[query] = compiled_query
        return compiled_query
