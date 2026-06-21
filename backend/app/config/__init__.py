from .config import (
    MAX_LOCAL_CAMERA_INDEX,
    MAX_QUEUE_SIZE,
    MAX_FRAME_QUEUE_SIZE,
    NOTIF_COOLDOWN,
    telegram_token,
    telegram_allowed_users,
    RECORD_TIMES
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
    "RECORD_TIMES",
    "RecordTime"
]
print("Loading configuration")
