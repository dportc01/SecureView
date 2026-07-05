import json
from pathlib import Path

from app.config import ConfigJson
from app.logging.loggers import get_files_logger


class ConfigurationService:
    def __init__(self, config_path: Path, initial_conf: ConfigJson) -> None:
        self.config_path = config_path
        self.logger = get_files_logger()
        # Initial conf is used to reflect that the conf doesn't apply until system restart
        self._config = initial_conf

    def get_configuration(self) -> ConfigJson:
        return self._config

    def update_configuration(self, config: dict) -> bool:
        try:
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=4)
            self.logger.info("Updated config file")
            return True

        except Exception as e:
            self.logger.exception(e)
            return False
