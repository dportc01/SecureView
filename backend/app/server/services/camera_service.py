import time
from importlib.resources import files

from app.messaging import BusInterface

NO_SIGNAL = files("app.assets").joinpath("no_signal.jpg").read_bytes()


class CameraService:
    def __init__(self, bus: BusInterface, cameras_ids: list[int]):
        self.bus = bus
        self.cameras_ids = cameras_ids
        self.last_frames: dict[int, bytes] = {
            camera_id: NO_SIGNAL for camera_id in cameras_ids
        }

    def start_camera(self, id: int) -> str | None:
        self.bus.send_start(id)

        return self._get_response()

    def stop_camera(self, id: int) -> str | None:
        self.bus.send_stop(id)

        response = self._get_response()

        # Empty remaining frames
        while self.bus.read_frame(id) is not None:
            pass

        self.last_frames[id] = NO_SIGNAL

        return response

    def terminate_cameras(self) -> str | None:
        self.bus.send_terminate()

        return self._get_response()

    def read_camera(self, id: int) -> bytes:
        frame = self.bus.read_frame(id)
        if frame is not None:
            self.last_frames[id] = frame
        return self.last_frames[id]

    def get_disovered_cameras(self):
        return self.cameras_ids

    def _get_response(self) -> str | None:
        # Retry to get response
        reponse = None
        for i in range(20):
            reponse = self.bus.read_response()
            if reponse is not None:
                break
            time.sleep(0.1)

        return reponse
