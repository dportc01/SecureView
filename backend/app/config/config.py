from dotenv import load_dotenv
import os

MAX_LOCAL_CAMERA_INDEX = 4
MAX_QUEUE_SIZE = 60


load_dotenv()
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")

raw = os.getenv("TELEGRAM_ALLOWED_USERS", "")
if raw is None:
    raise RuntimeError("Missing enviromental variable TELEGRAM_ALLOWED_USERS")
telegram_allowed_users = [x.strip() for x in raw.split(",") if x.strip()]

if telegram_token is None:
    raise RuntimeError("Missing enviromental variable TELEGRAM_BOT_TOKEN")
