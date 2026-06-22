import cv2
import time
import numpy as np


class Recorder():
    def __init__(self) -> None:
        self.format = ".mp4"
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # type: ignore[attr-defined]
        self.out: cv2.VideoWriter

    def start_record(self, camera_id: int, height: int, width: int) -> None:
        filename = f"camera{camera_id}_{time.time()}{self.format}"
        self.out = cv2.VideoWriter(filename, self.fourcc, 30, (width, height))
        if not self.out.isOpened():
            raise RuntimeError("VideoWriter failed to open")

    def insert_frame(self, frame: np.ndarray) -> None:
        self.out.write(frame)

    def stop_record(self) -> None:
        self.out.release()
