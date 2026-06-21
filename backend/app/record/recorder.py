import cv2
import time
import numpy as np
from app.logging.loggers import get_record_logger


class Recorder():
    def __init__(self, camera_id: int) -> None:
        self.camera_id = camera_id
        self.format = ".mp4"
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # type: ignore[attr-defined]
        self.out: cv2.VideoWriter
        self.logger = get_record_logger(camera_id)

    def start_record(self):
        filename = f"camera{self.camera_id}_{time.time()}{self.format}"
        self.out = cv2.VideoWriter(filename, self.fourcc, 30, (960, 540))

    def insert_frame(self, frame: np.ndarray) -> None:
        self.out.write(frame)

    def stop_record(self) -> None:
        self.out.release()
