# from app.workers.record_woker import record_woker
# from app.record import Command, Type
# from tests.integration.recorder_mock import RecorderMock
# from multiprocessing import Queue, Process
# import pytest
# import numpy as np
# import time


# @pytest.fixture
# def pre_build():
#     mock = RecorderMock()
#     queue = Queue()
#     p = Process(target=record_woker, args=(mock, queue, 0))
#     p.start()

#     yield mock, queue

#     queue.put(Command(Type.TERMINATE, None))
#     p.join()


# def test_start_record(pre_build):
#     mock, queue = pre_build
#     assert mock.recording is False

#     queue.put(Command(Type.START, None))
#     time.sleep(1)
#     assert mock.recording is True


# def test_send_frame(pre_build):
#     mock, queue = pre_build
#     queue.put(Command(Type.FRAME, np.array([])))
#     time.sleep(0.1)
#     assert mock.frame_recieved is False

#     queue.put(Command(Type.START, None))
#     queue.put(Command(Type.FRAME, np.array([])))
#     time.sleep(0.1)
#     assert mock.frame_recieved is True


# def test_stop_record(pre_build):
#     mock, queue = pre_build
#     assert mock.recording is False

#     queue.put(Command(Type.START, None))
#     time.sleep(0.1)
#     assert mock.recording is True

#     queue.put(Command(Type.STOP, None))
#     time.sleep(0.1)
#     assert mock.recording is False


# def test_no_frame(pre_build):
#     mock, queue = pre_build
#     queue.put(Command(Type.START, None))
#     time.sleep(0.1)
#     assert mock.recording is True

#     queue.put(Command(Type.FRAME, None))
#     time.sleep(0.1)
#     assert mock.frame_recieved is False
