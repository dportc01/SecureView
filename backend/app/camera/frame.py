from dataclasses import dataclass
import numpy as np
import cv2


@dataclass
class Frame:
    data: np.ndarray
    width: int
    height: int

    def to_bytes(self) -> bytes:
        _, buffer = cv2.imencode(".jpg", self.data)
        return buffer.tobytes()
