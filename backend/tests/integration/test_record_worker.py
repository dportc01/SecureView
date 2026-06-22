from app.workers.record_woker import record_woker
from app.record import Command, Type
from tests.integration.recorder_mock import RecorderMock
from multiprocessing import Queue, Process, Manager
import numpy as np
import pytest
import time


@pytest.fixture(scope="function")
def set_up_tests():
    manager = Manager()
    state = manager.dict({
        "recording": False,
        "frame_received": False
    })
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

    queue.put(Command(Type.START, None))
    time.sleep(0.3)
    assert state["recording"] is True


def test_send_frame(set_up_tests):
    state, queue = set_up_tests
    queue.put(Command(Type.FRAME, np.array([])))
    time.sleep(0.3)
    assert state["frame_received"] is False

    queue.put(Command(Type.START, None))
    time.sleep(0.3)
    queue.put(Command(Type.FRAME, np.array([])))
    time.sleep(0.3)
    assert state["recording"] is True


def test_stop_record(set_up_tests):
    state, queue = set_up_tests
    assert state["recording"] is False

    queue.put(Command(Type.START, None))
    time.sleep(0.3)
    assert state["recording"] is True

    queue.put(Command(Type.STOP, None))
    time.sleep(0.3)
    assert state["recording"] is False


def test_no_frame(set_up_tests):
    state, queue = set_up_tests
    queue.put(Command(Type.START, None))
    time.sleep(0.3)
    assert state["recording"] is True

    queue.put(Command(Type.FRAME, None))
    time.sleep(0.3)
    assert state["frame_received"] is False
