from app.record import Recorder


class RecorderMock(Recorder):
    def __init__(self, state):
        self.state = state

    def start_record(self, id):
        self.state["recording"] = True

    def insert_frame(self, frame):
        self.state["frame_received"] = True

    def stop_record(self):
        self.state["recording"] = False
