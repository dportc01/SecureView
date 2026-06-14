from multiprocessing import Queue
from queue import Empty
from .messages import Command, Action

class InvalidQueueIndexError(Exception):
    pass

class MutiprocessingBus():
    def __init__(self, queues: list[Queue]) -> None:
        self.queue_size = len(queues)
        self.queues = queues

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
        
    def send(self, id: int, action: Action) -> None:
        if 0 <= id < self.queue_size:
            cmd = Command(
                dev_id=id,
                action=action
            )
            self.queues[id].put(cmd)
        else:
            raise InvalidQueueIndexError(f"Error: invalid queue id {id}")