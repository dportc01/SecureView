from app.config import CONF_JSON, ConfigJson, CONFIG_JSON_PATH
import json
import logging


class ConfigurationService:
    def get_configuration(self) -> ConfigJson:
        return CONF_JSON

    def update_configuration(self, config: dict) -> bool:
        try:
            with open(CONFIG_JSON_PATH, "w") as f:
                json.dump(config, f, indent=4)
            return True

        except Exception as e:
            logging.exception(e)
            return False
