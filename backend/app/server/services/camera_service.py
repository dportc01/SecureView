from app.messaging import BusInterface
import time


class CameraService:
    def __init__(self, bus: BusInterface, cameras_ids: list[int]):
        self.bus = bus
        self.cameras_ids = cameras_ids

    def start_camera(self, id: int) -> str | None:
        self.bus.send_start(id)

        return self._get_response()

    def stop_camera(self, id: int) -> str | None:
        self.bus.send_stop(id)

        return self._get_response()

    def terminate_cameras(self) -> str | None:
        self.bus.send_terminate()

        return self._get_response()

    def read_camera(self, id: int) -> bytes | None:
        return self.bus.read_frame(id)

    def get_disovered_cameras(self):
        return self.cameras_ids

    def _get_response(self) -> str | None:
        # Retry to get response
        reponse = None
        for i in range(10):
            reponse = self.bus.read_response()
            if reponse is not None:
                break
            time.sleep(0.1)

        return reponse
