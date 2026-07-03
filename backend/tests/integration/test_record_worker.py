# This tests are mostly falky and depend on the computer processing power

from multiprocessing import Queue, Process, Manager
import numpy as np
import pytest
import time

from app.workers.record_woker import record_woker
from app.record import Command, Type
from tests.integration.recorder_mock import RecorderMock


@pytest.fixture(scope="function")
def set_up_tests():
    manager = Manager()
    state = manager.dict({"recording": False, "frame_received": False})
    mock = RecorderMock(state)
    queue = Queue()
    p = Process(target=record_woker, args=(mock, queue, 0))
    p.start()

    yield state, queue

    queue.put(Command(Type.TERMINATE, None))
    p.join()


def test_start_record(set_up_tests):
    state, queue = set_up_tests
    assert state["recording"] is False

    queue.put(Command(Type.FRAME, np.zeros((540, 960, 3), dtype=np.uint8)))
    time.sleep(0.5)
    assert state["recording"] is True


def test_stop_record(set_up_tests):
    state, queue = set_up_tests
    assert state["recording"] is False

    queue.put(Command(Type.FRAME, np.zeros((540, 960, 3), dtype=np.uint8)))
    time.sleep(0.5)
    assert state["recording"] is True

    queue.put(Command(Type.STOP, None))
    time.sleep(0.5)
    assert state["recording"] is False


def test_terminate_record(set_up_tests):
    state, queue = set_up_tests
    queue.put(Command(Type.FRAME, np.zeros((540, 960, 3), dtype=np.uint8)))
    time.sleep(0.5)
    assert state["recording"] is True

    queue.put(Command(Type.TERMINATE, None))
    time.sleep(0.5)
    assert state["recording"] is False


def test_no_frame(set_up_tests):
    state, queue = set_up_tests
    queue.put(Command(Type.FRAME, None))
    time.sleep(0.5)
    assert state["recording"] is False
