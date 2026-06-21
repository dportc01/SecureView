import numpy as np
from app.record import Recorder


class RecorderMock(Recorder):
    def start_record(self):
        pass

    def insert_frame(self, frame: np.ndarray) -> None:
        pass

    def stop_record(self) -> None:
        pass
