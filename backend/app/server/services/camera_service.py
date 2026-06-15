from app.messaging import BusInterface
from typing import Iterable


class CameraService:
    def __init__(self, bus: BusInterface):
        self.bus = bus

    def start_camera(self, id: int):
        self.bus.send_start(id)

    def read_camera(self, id: int) -> Iterable[bytes]:
        yield from (self.bus.read_fame_stream(id))
