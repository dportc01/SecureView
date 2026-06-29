from app.config import CONF_JSON, ConfigJson


class ConfigurationService:
    def get_configuration(self) -> ConfigJson:
        return CONF_JSON
