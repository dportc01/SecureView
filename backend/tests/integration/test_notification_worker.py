import pytest
import time
from app.workers.notification_worker import notification_worker
from app.notification import MockNotification, Command, Type
from multiprocessing import Queue


@pytest.fixture
def pre_build():
    mock = MockNotification()
    queue = Queue()
    thread = notification_worker(mock, queue)

    yield mock, queue

    queue.put(Command(Type.TERMINATE, None, None))
    thread.join()


def test_send_msg(pre_build):
    mock, queue = pre_build
    queue.put(Command(Type.MESSAGE, "msg", None))
    time.sleep(0.1)
    assert mock.msg_called is True


def test_send_img(pre_build):
    mock, queue = pre_build
    queue.put(Command(Type.IMAGE, "msg", b"bytes"))
    time.sleep(0.1)
    assert mock.img_called is True


def test_none_msg(pre_build):
    mock, queue = pre_build
    queue.put(Command(Type.MESSAGE, None, None))
    assert mock.msg_called is False


def test_none_img(pre_build):
    mock, queue = pre_build
    queue.put(Command(Type.IMAGE, "msg", None))
    assert mock.img_called is False

    queue.put(Command(Type.IMAGE, None, b"bytes"))
    assert mock.img_called is False
