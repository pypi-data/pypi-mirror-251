from k8s_collector.config.models import CollectorConfig, Resource, Selector, Entity, EntityMapping
from k8s_collector.config.models.sinks import SinkConfig
from k8s_collector.config.parsers.collector_config_parser import CollectorConfigParser
from k8s_collector.config.parsers.exceptions import ParseError
from k8s_collector.config.parsers.sinks import SinkConfigParser
from k8s_collector.config.parsers.sinks.factory import SinkConfigParserFactory
from k8s_collector.config.validators import CollectorConfigValidator


class DictCollectorConfigParser(CollectorConfigParser):
    def __init__(self, collector_config_validator: CollectorConfigValidator, sink_config_parser_factory: SinkConfigParserFactory):
        self._collector_config_validator = collector_config_validator
        self._sink_config_parser_factory = sink_config_parser_factory

    def parse(self, obj: dict) -> CollectorConfig:
        self._collector_config_validator.validate(obj)
        try:
            resources: list[dict] = obj['resources']
            resources: list[Resource] = [self._parse_resource(resource) for resource in resources]
            return CollectorConfig(resources=resources)
        except KeyError as err:
            raise ParseError(f"Couldn't find key {err} in config, check your config") from err

    def _parse_resource(self, resource: dict) -> Resource:
        api_version: str = resource['apiVersion']
        kind: str = resource['kind']
        selector: Selector = self._parse_selector(resource)
        entity: Entity = self._parse_entity(resource)
        sink_configs: list[SinkConfig] = self._parse_sink_config(resource)
        return Resource(api_version=api_version, kind=kind, selector=selector, entity=entity, sinks=sink_configs)

    def _parse_selector(self, resource: dict) -> Selector:
        query: str = resource['selector']['query']
        return Selector(query=query)

    def _parse_entity(self, resource: dict) -> Entity:
        mappings: list[dict] = resource['entity']['mappings']
        entity_mappings: list[EntityMapping] = [self._parse_entity_mapping(mapping) for mapping in mappings]
        entity: Entity = Entity(mappings=entity_mappings)
        return entity

    def _parse_entity_mapping(self, mapping: dict) -> EntityMapping:
        return EntityMapping(identifier=mapping['identifier'],
                             title=mapping['title'],
                             blueprint=mapping['blueprint'],
                             team=mapping['team'],
                             properties=mapping['properties'],
                             relations=mapping.get('relations'))

    def _parse_sink_config(self, resource: dict) -> list[SinkConfig]:
        sinks_obj: list[dict] = resource['sinks']
        sink_configs: list[SinkConfig] = []
        for sink_obj in sinks_obj:
            sink_config_parser: SinkConfigParser = self._sink_config_parser_factory.get_sink_config_parser(sink_obj)
            sink_config: SinkConfig = sink_config_parser.parse(sink_obj)
            sink_configs.append(sink_config)

        return sink_configs


