from app.config import CONF_JSON, ConfigJson, CONFIG_JSON_PATH
from app.logging.loggers import get_files_logger
import json


class ConfigurationService:
    def __init__(self) -> None:
        self.logger = get_files_logger()

    def get_configuration(self) -> ConfigJson:
        return CONF_JSON

    def update_configuration(self, config: dict) -> bool:
        try:
            with open(CONFIG_JSON_PATH, "w") as f:
                json.dump(config, f, indent=4)
            self.logger.info("Updated config file")
            return True

        except Exception as e:
            self.logger.exception(e)
            return False
