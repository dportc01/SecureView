from typing import Iterable


class MockCamera:
    def __init__(self) -> None:
        pass

    def start_capture(self) -> Iterable[bytes]:
        print("Capture process begins")
        return [b"frame1", b"frame2", b"frame3"]

    def stop_capture(self) -> None:
        print("Capture process stop")