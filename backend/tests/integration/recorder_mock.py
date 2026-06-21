import numpy as np
from app.record import Recorder


class RecorderMock(Recorder):
    def __init__(self) -> None:
        self.recording = False
        self.frame_recieved = False

    def start_record(self, id: int) -> None:
        print("Started recording")
        self.recording = True
        print(self.recording)

    def insert_frame(self, frame: np.ndarray) -> None:
        self.frame_recieved = True

    def stop_record(self) -> None:
        self.recording = False
