import json
from pathlib import Path
from app.config import ConfigJson, NOTIF_COOLDOWN, CONFIG_JSON_PATH


class ConfigurationService:
    def get_configuration(self) -> ConfigJson:
        config_json_path = Path(__file__).with_name("config.json")

        # No need to check, application already stops on start up on missing config
        # file (config.py)

        with open(config_json_path) as f:
            data = json.load(f)

            return ConfigJson(
                notification_time=data.get("notification_time", DEFAULT_NOTIF_TIME),
                cameras=data["cameras"]
            )
