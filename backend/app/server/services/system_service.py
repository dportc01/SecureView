from multiprocessing import Queue
from queue import Full


class SystemService:
    def __init__(self, queue: Queue) -> None:
        self.queue = queue

    def terminate_system(self) -> bool:
        try:
            self.queue.put_nowait(False)
            return True
        except Full, ValueError:
            return False

    def restart_system(self) -> bool:
        try:
            self.queue.put_nowait(True)
            return True
        except Full, ValueError:
            return False
