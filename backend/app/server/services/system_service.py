from multiprocessing import Queue
from queue import Full

from app.logging.loggers import get_system_logger


class SystemService:
    def __init__(self, queue: Queue) -> None:
        self.queue = queue
        self.logger = get_system_logger()

    def terminate_system(self) -> bool:
        try:
            self.queue.put_nowait(False)
            return True
        except (Full, ValueError) as e:
            print(e)
            self.logger.exception(e)
            return False

    def restart_system(self) -> bool:
        try:
            self.queue.put_nowait(True)
            return True
        except (Full, ValueError) as e:
            print(e)
            self.logger.exception(e)
            return False
