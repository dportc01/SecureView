from typing import Protocol, Iterable
from dataclasses import dataclass
import numpy as np


@dataclass
class Frame:
    data: np.ndarray
    data_bytes: bytes
    width: int
    height: int


class CameraInterface(Protocol):
    def start_capture(self) -> Iterable[Frame]:
        ...

    def stop_capture(self) -> None:
        ...
