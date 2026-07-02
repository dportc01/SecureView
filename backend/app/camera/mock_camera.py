from typing import Iterable
from .frame import Frame
import time
import numpy as np


class MockCamera:
    def __init__(self) -> None:
        self.capturing: bool
        self.open: bool
        pass

    def open_camera(self) -> None:
        self.open = True

    def start_capture(self) -> Iterable[Frame]:
        print("Capture process begins")
        self.capturing = True
        while self.capturing:
            frame = np.random.randint(
                0, 255, (300, 400, 3), dtype=np.uint8
            )
            yield Frame(
                data=frame,
                width=400,
                height=300
            )
            time.sleep(0.008)  # 120 FPS

    def stop_camera(self) -> None:
        print("Capture process stop")
        self.capturing = False
        self.open = False
