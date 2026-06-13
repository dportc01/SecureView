from typing import Protocol


class CameraInterface(Protocol):
    def get_camera_count(self) -> int:
        ...
