from app.messaging import BusInterface


class CameraService:
    def __init__(self, bus: BusInterface):
        self.bus = bus

    def start_camera(self, id: int):
        self.bus.send_start(id)

    def read_camera(self, id: int) -> bytes | None:
        return self.bus.read_frame(id)
