from multiprocessing import Queue
from queue import Empty
from .messages import Command, Action
from app.config import MAX_QUEUE_SIZE


class InvalidQueueIndexError(Exception):
    pass


class MutiprocessingBus:
    def __init__(self, camera_num: int) -> None:
        self.queues = [Queue(MAX_QUEUE_SIZE)] * camera_num
        self.res_queue = Queue()
        self.frames_queues = [Queue(MAX_QUEUE_SIZE)] * camera_num
        self.queue_size = camera_num

    def send_start(self, id: int) -> None:
        self.send(id, Action.START)

    def send_stop(self, id: int) -> None:
        self.send(id, Action.STOP)

    def send_terminate(self) -> None:
        for i in range(self.queue_size):
            cmd = Command(
                dev_id=i,
                action=Action.TERMINATE
            )
            self.queues[i].put(cmd)

    def recv(self, id: int) -> Action:
        if 0 <= id < self.queue_size:
            try:
                msg: Command = self.queues[id].get_nowait()
                return msg.action
            except Empty:
                return Action.Empty
        else:
            raise InvalidQueueIndexError(f"Error: invalid queue id {id}")

    def write_frame(self, id: int, frame: bytes) -> None:
        if 0 <= id < self.queue_size:
            self.frames_queues[id].put(frame)
        else:
            raise InvalidQueueIndexError(f"Error: invalid queue id {id}")

    def read_frame(self, id: int) -> bytes:
        if 0 <= id < self.queue_size:
            try:
                frame: bytes = self.frames_queues[id].get_nowait()
                return frame
            except Empty:
                return b'No frame data'
        else:
            raise InvalidQueueIndexError(f"Error: invalid queue id {id}")

    def respond(self, response: str) -> None:
        self.res_queue.put(str)

    # TODO: Finish this function
    def read_response(self) -> str:
        return "N"

    def send(self, id: int, action: Action) -> None:
        if 0 <= id < self.queue_size:
            cmd = Command(
                dev_id=id,
                action=action
            )
            self.queues[id].put(cmd)
        else:
            raise InvalidQueueIndexError(f"Error: invalid queue id {id}")
