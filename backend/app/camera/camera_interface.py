from typing import Protocol, Iterable
from .frame import Frame


class CameraInterface(Protocol):
    def start_capture(self) -> Iterable[Frame]:
        ...

    def stop_capture(self) -> None:
        ...
