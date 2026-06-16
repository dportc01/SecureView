from typing import Iterable
import time


class MockCamera:
    def __init__(self) -> None:
        self.capturing: bool
        pass

    def start_capture(self) -> Iterable[bytes]:
        print("Capture process begins")
        self.capturing = True
        while self.capturing:
            rand = str(time.time()).encode()
            yield b"frame1_" + rand
            time.sleep(0.008)  # 120 FPS

    def stop_capture(self) -> None:
        print("Capture process stop")
        self.capturing = False
