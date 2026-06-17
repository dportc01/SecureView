from multiprocessing import Queue
from queue import Empty
from .messages import Command, Action
from app.discovery import CameraData
from app.config import MAX_QUEUE_SIZE


class InvalidQueueIndexError(Exception):
    pass


class MutiprocessingBus:
    def __init__(self, cameras_data: list[CameraData]) -> None:
        self.queues = {
            cam["id"]: Queue(MAX_QUEUE_SIZE)
            for cam in cameras_data
        }
        self.frames_queues = {
            cam["id"]: Queue(MAX_QUEUE_SIZE)
            for cam in cameras_data
        }
        self.res_queue = Queue()

    def send_start(self, id: int) -> None:
        self._send(id, Action.START)

    def send_stop(self, id: int) -> None:
        self._send(id, Action.STOP)

    def send_terminate(self) -> None:
        for id, queue in self.queues.items():
            cmd = Command(
                dev_id=id,
                action=Action.TERMINATE
            )
            queue.put(cmd)

    def cam_recv(self, id: int) -> Action | None:
        queue = self._get_queue(id)
        try:
            msg: Command = queue.get_nowait()
            return msg.action
        except Empty:
            return None

    def write_frame(self, id: int, frame: bytes) -> None:
        queue = self._get_frames_queue(id)
        # If full drop oldest frame
        if queue.full():
            try:
                queue.get()
            except Empty:
                pass

        queue.put(frame)

    def read_frame(self, id: int) -> bytes | None:
        queue = self._get_frames_queue(id)
        try:
            frame: bytes = queue.get_nowait()
            return frame
        except Empty:
            return None

    def respond(self, response: str) -> None:
        self.res_queue.put(response)

    def read_response(self) -> str | None:
        try:
            return self.res_queue.get_nowait()
        except Empty:
            return None

    def close(self):
        for q in self.queues.values():
            q.close()
            q.cancel_join_thread()
        for q in self.frames_queues.values():
            q.close()
            q.cancel_join_thread()

    def _send(self, id: int, action: Action) -> None:
        queue = self._get_queue(id)

        cmd = Command(
            dev_id=id,
            action=action
        )

        queue.put(cmd)

    def _get_queue(self, id: int) -> Queue:
        try:
            return self.queues[id]
        except KeyError:
            raise InvalidQueueIndexError(f"Error: invalid queue id {id}")

    def _get_frames_queue(self, id: int) -> Queue:
        try:
            return self.frames_queues[id]
        except KeyError:
            raise InvalidQueueIndexError(f"Error: invalid queue id {id}")
