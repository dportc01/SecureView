import cv2
from datetime import datetime
import numpy as np
import os


class Recorder():
    def __init__(self) -> None:
        self.format = ".mp4"
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # type: ignore[attr-defined]
        self.out: cv2.VideoWriter
        self.output_dir = "video_records"

    def start_record(self, camera_id: int, height: int, width: int) -> None:
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        now = datetime.now()
        date = now.strftime("%d.%m.%y_%H-%M-%S.%f")

        filename = f"camera{camera_id}_{date}{self.format}"
        filepath = os.path.join(self.output_dir, filename)

        self.out = cv2.VideoWriter(filepath, self.fourcc, 30, (width, height))

        if not self.out.isOpened():
            raise RuntimeError("VideoWriter failed to open")

    def insert_frame(self, frame: np.ndarray) -> None:
        self.out.write(frame)

    def stop_record(self) -> None:
        self.out.release()
