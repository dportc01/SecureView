from typing import Protocol


class CameraInterface(Protocol):
    def capture(self) -> None:
        ...
