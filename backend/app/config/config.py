from dotenv import load_dotenv
from pathlib import Path
import logging
import os
import json
from datetime import time
from .config_types import RecordTime, ConfigJson, ConfigJsonCam

# Queue
MAX_LOCAL_CAMERA_INDEX = 4
MAX_FRAME_QUEUE_SIZE = 60
MAX_QUEUE_SIZE = 10


# Env vars
load_dotenv()

raw = os.getenv("TELEGRAM_BOT_TOKEN")
if not raw:
    logging.error("Missing enviromental variable TELEGRAM_BOT_TOKEN")
telegram_token = raw

raw = os.getenv("TELEGRAM_ALLOWED_USERS")
if not raw:
    logging.error("Missing enviromental variable TELEGRAM_ALLOWED_USERS")
    telegram_allowed_users = raw
else:
    telegram_allowed_users = [x.strip() for x in raw.split(",") if x.strip()]

cors_allow_url = os.getenv("FRONTEND_URL", "*")

# Open ./config.json
CONFIG_JSON_PATH = Path(__file__).with_name("config.json")

if not CONFIG_JSON_PATH.exists():
    raise RuntimeError(f"Missing config.json file on {CONFIG_JSON_PATH}")

with open(CONFIG_JSON_PATH) as f:
    data = json.load(f)


# Notfication
SECOND = 1
MINUTE = 60 * SECOND

DEFAULT_NOTIF_TIME = 10

NOTIF_COOLDOWN = data.get("notification_time", DEFAULT_NOTIF_TIME) * MINUTE


# Recording
def parse_time(t: str) -> time:
    h, m = map(int, t.split(":"))
    return time(hour=h, minute=m)


RECORD_TIMES: dict[int, RecordTime] = {}
camera_config: list[ConfigJsonCam] = []
RECORD_DIR = "video_records"

if "cameras" in data:
    for cam in data["cameras"]:
        RECORD_TIMES[cam["id"]] = RecordTime(
            start=parse_time(cam["start_record"]),
            end=parse_time(cam["end_record"]),
        )
        camera_config.append(
            ConfigJsonCam(
                id=cam["id"],
                start_record=cam["start_record"],
                end_record=cam["end_record"],
            )
        )


# Data for configuration api
CONF_JSON = ConfigJson(notification_time=NOTIF_COOLDOWN / MINUTE, cameras=camera_config)
