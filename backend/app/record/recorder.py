import cv2
from datetime import datetime
import numpy as np
from pathlib import Path


class Recorder:
    def __init__(self, record_dir: Path) -> None:
        self.format = ".mp4"
        self.record_dir = record_dir
        self.filepath: Path | None = None
        self.final_path: Path | None = None
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # type: ignore[attr-defined]
        self.out: cv2.VideoWriter

    def start_record(self, camera_id: int, height: int, width: int) -> None:
        self.record_dir.mkdir(parents=True, exist_ok=True)

        now = datetime.now()
        date = now.strftime("%d.%m.%y_%H-%M-%S.%f")

        filename = f"camera{camera_id}_{date}"
        self.filepath = self.record_dir / f"{filename}.tmp{self.format}"
        self.final_path = self.record_dir / f"{filename}{self.format}"

        self.out = cv2.VideoWriter(str(self.filepath), self.fourcc, 30, (width, height))

        if not self.out.isOpened():
            raise RuntimeError("VideoWriter failed to open")

    def insert_frame(self, frame: np.ndarray) -> None:
        self.out.write(frame)

    def stop_record(self) -> None:
        self.out.release()
        if self.filepath and self.final_path:
            self.filepath.rename(self.final_path)
            self.filepath = None
            self.final_path = None
