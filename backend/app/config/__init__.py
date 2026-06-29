from .config import (
    MAX_LOCAL_CAMERA_INDEX,
    MAX_QUEUE_SIZE,
    MAX_FRAME_QUEUE_SIZE,
    NOTIF_COOLDOWN,
    telegram_token,
    telegram_allowed_users,
    cors_allow_url,
    CONFIG_JSON_PATH,
    RECORD_TIMES,
    RECORD_DIR,
    CONF_JSON,
)

from .config_types import (
    RecordTime,
    ConfigJson,
)

__all__ = [
    "MAX_LOCAL_CAMERA_INDEX",
    "MAX_QUEUE_SIZE",
    "MAX_FRAME_QUEUE_SIZE",
    "NOTIF_COOLDOWN",
    "telegram_token",
    "telegram_allowed_users",
    "cors_allow_url",
    "CONFIG_JSON_PATH",
    "RECORD_TIMES",
    "RecordTime",
    "RECORD_DIR",
    "ConfigJson",
    "CONF_JSON",
]
