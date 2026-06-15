from app.messaging import BusInterface


class CameraService:
    def __init__(self, bus: BusInterface):
        self.bus = bus

    def start_camera(self, id: int) -> str | None:
        self.bus.send_start(id)

        return self._get_response()

    def stop_camera(self, id: int) -> str | None:
        self.bus.send_stop(id)

        return self._get_response()

    def read_camera(self, id: int) -> bytes | None:
        return self.bus.read_frame(id)

    def _get_response(self) -> str | None:
        # Retry to get response
        for i in range(10):
            reponse = self.bus.read_response()
            if reponse is not None:
                break

        return reponse
