from pathlib import Path

import yaml

from k8s_collector.config.models import CollectorConfig
from k8s_collector.config.parsers.dict_collector_config_parser import DictCollectorConfigParser


class YamlCollectorConfigParser(DictCollectorConfigParser):
    def parse(self, obj: dict) -> CollectorConfig:
        return super().parse(obj)

    def parse_file(self, config_file_path: str | Path) -> CollectorConfig:
        config_file_path = Path(config_file_path)
        with open(config_file_path, mode='r') as file:
            collector_config: dict = yaml.safe_load(file)
        return self.parse(collector_config)
