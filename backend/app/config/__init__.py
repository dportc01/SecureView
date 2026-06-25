from .config import (
    MAX_LOCAL_CAMERA_INDEX,
    MAX_QUEUE_SIZE,
    MAX_FRAME_QUEUE_SIZE,
    NOTIF_COOLDOWN,
    telegram_token,
    telegram_allowed_users,
    cors_allow_url,
    RECORD_TIMES,
    RECORD_DIR,
)

from .config_types import (
    RecordTime
)

__all__ = [
    "MAX_LOCAL_CAMERA_INDEX",
    "MAX_QUEUE_SIZE",
    "MAX_FRAME_QUEUE_SIZE",
    "NOTIF_COOLDOWN",
    "telegram_token",
    "telegram_allowed_users",
    "cors_allow_url",
    "RECORD_TIMES",
    "RecordTime",
    "RECORD_DIR"
]
