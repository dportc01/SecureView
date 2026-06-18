from dotenv import load_dotenv
import os

MAX_LOCAL_CAMERA_INDEX = 4
MAX_QUEUE_SIZE = 60


load_dotenv()

raw = os.getenv("TELEGRAM_BOT_TOKEN")
if raw is None:
    raise RuntimeError("Missing enviromental variable TELEGRAM_BOT_TOKEN")
telegram_token = raw

raw = os.getenv("TELEGRAM_ALLOWED_USERS", "")
if raw is None:
    raise RuntimeError("Missing enviromental variable TELEGRAM_ALLOWED_USERS")
telegram_allowed_users = [x.strip() for x in raw.split(",") if x.strip()]
