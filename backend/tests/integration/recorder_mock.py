from app.record import Recorder


class RecorderMock(Recorder):
    def __init__(self, state):
        self.state = state

    def start_record(self, camera_id: int, height: int, width: int) -> None:
        ...

    def insert_frame(self, frame):
        self.state["recording"] = True

    def stop_record(self):
        self.state["recording"] = False
