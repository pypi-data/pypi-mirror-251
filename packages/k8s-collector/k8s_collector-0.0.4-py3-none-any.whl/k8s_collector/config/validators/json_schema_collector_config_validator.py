import json
from pathlib import Path

import jsonschema
from jsonschema.exceptions import ValidationError, SchemaError

from k8s_collector.config.validators.collector_config_validator import CollectorConfigValidator


class JsonSchemaCollectorConfigValidator(CollectorConfigValidator):
    def __init__(self, collector_config_schema_file_path: str | Path):
        self._collector_config_schema_file_path = Path(collector_config_schema_file_path)
        with open(self._collector_config_schema_file_path, mode='r') as file:
            self._collector_config_schema: dict = json.load(file)

    def validate(self, config: dict) -> None:
        jsonschema.validate(config, self._collector_config_schema)

    def is_valid(self, config: dict) -> bool:
        try:
            self.validate(config)
            return True
        except (ValidationError, SchemaError):
            return False
