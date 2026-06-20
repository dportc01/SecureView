from threading import Thread
from multiprocessing import Queue
import asyncio
from app.notification import NotificationInterface, Command, Type
from app.logging.loggers import get_notification_logger


def notification_worker(notifier: NotificationInterface, queue: Queue) -> Thread:

    logger = get_notification_logger()

    def start_woker():
        async def loop():
            alive = True

            while alive:
                cmd: Command = queue.get()

                if cmd.type == Type.MESSAGE:
                    if cmd.msg is None:
                        logger.error("There was no message attached")
                    else:
                        await notifier.notify_msg(cmd.msg)

                if cmd.type == Type.IMAGE:
                    if cmd.img is None or cmd.msg is None:
                        logger.error("There was no sufficient data attached")
                    else:
                        await notifier.notify_img(cmd.msg, cmd.img)

                if cmd.type == Type.TERMINATE:
                    alive = False

        asyncio.run(loop())

    thread = Thread(target=start_woker, daemon=True)
    thread.start()
    return thread
