from typing import Iterable


class MockCamera:
    def __init__(self) -> None:
        pass

    def start_capture(self) -> Iterable[bytes]:
        print("Capture process begins")
        yield b"frame1"
        yield b"frame2"
        yield b"frame3"

    def stop_capture(self) -> None:
        print("Capture process stop")
