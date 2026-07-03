from telegram import Bot
from telegram.error import TelegramError
from io import BytesIO

from app.logging.loggers import get_notification_logger
from app.config import telegram_token, telegram_allowed_users


class TelegramNotification:
    def __init__(self) -> None:
        if telegram_token is None:
            raise RuntimeError("Missing telegram bot token")
        self.bot = Bot(token=telegram_token)
        self.logger = get_notification_logger()

    async def notify_msg(self, msg: str) -> None:
        for user_id in telegram_allowed_users:
            try:
                result = await self.bot.send_message(chat_id=user_id, text=msg)
                self.logger.info(f"Sent notification {result.message_id} to {user_id}")
            except TelegramError as e:
                self.logger.exception(f"Couldn't notify {user_id}: {e}")

    async def notify_img(self, attached_msg: str, img: bytes) -> None:
        bio = BytesIO(img)
        bio.name = "image.jpg"

        for user_id in telegram_allowed_users:
            try:
                result = await self.bot.send_photo(
                    chat_id=user_id, photo=bio, caption=attached_msg
                )
                self.logger.info(
                    f"Sent notification image {result.message_id} to {user_id}"
                )
                bio.seek(0)  # TODO: Check better method for reseting buffer
            except TelegramError as e:
                self.logger.exception(f"Couldn't send image to {user_id}: {e}")
