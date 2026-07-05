import numpy as np

from app.record import Recorder


def test_record_cycle(tmp_path):
    recorder = Recorder(tmp_path)

    recorder.start_record(0, 1080, 720)

    files = list(tmp_path.glob("*.tmp.mp4"))
    assert len(files) == 1

    recorder.insert_frame(np.zeros((540, 960, 3), dtype=np.uint8))
    recorder.stop_record()

    files = list(tmp_path.glob("*.tmp.mp4"))
    assert len(files) == 0
    files = list(tmp_path.glob("*.mp4"))
    assert len(files) == 1
