from dotenv import load_dotenv
from pathlib import Path
import logging
import os
import json
from datetime import time
from .config_types import RecordTime

# Queue
MAX_LOCAL_CAMERA_INDEX = 4
MAX_FRAME_QUEUE_SIZE = 60
MAX_QUEUE_SIZE = 10

load_dotenv()

raw = os.getenv("TELEGRAM_BOT_TOKEN")
if raw is None:
    logging.error("Missing enviromental variable TELEGRAM_BOT_TOKEN")
telegram_token = raw

raw = os.getenv("TELEGRAM_ALLOWED_USERS", "")
if raw is None:
    logging.error("Missing enviromental variable TELEGRAM_ALLOWED_USERS")
telegram_allowed_users = [x.strip() for x in raw.split(",") if x.strip()]


# Open SecureView/data/config.json
base_dir = Path(__file__).resolve().parents[2]
config_json_path = base_dir / "data" / "config.json"

if not config_json_path.exists():
    raise RuntimeError(f"Missing config.json file on {config_json_path}")

with open(config_json_path) as f:
    data = json.load(f)


# Notfication
SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE

NOTIF_COOLDOWN = data.get("notification_time", 10) * MINUTE


# Recording
def parse_time(t: str) -> time:
    h, m = map(int, t.split(":"))
    return time(hour=h, minute=m)


RECORD_TIMES: dict[int, RecordTime] = {}

if "cameras" in data:
    for cam in data["cameras"]:
        RECORD_TIMES[cam["id"]] = RecordTime(
            start=parse_time(cam["start_record"]),
            end=parse_time(cam["start_record"]),
        )
