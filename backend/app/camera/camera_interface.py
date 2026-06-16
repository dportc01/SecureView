from typing import Protocol, Iterable


class CameraInterface(Protocol):
    def start_capture(self) -> Iterable[bytes]:
        ...

    def stop_capture(self) -> None:
        ...
