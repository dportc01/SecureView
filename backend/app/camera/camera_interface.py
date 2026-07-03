from typing import Protocol, Iterable
from .frame import Frame


class CameraInterface(Protocol):
    def start_capture(self) -> Iterable[Frame]: ...

    def open_camera(self) -> None: ...

    def stop_camera(self) -> None: ...
