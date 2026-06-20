from app.discovery import CameraData, CameraType
from app.messaging import MutiprocessingBus
from app.workers import start_workers
from app.notification import MockNotification
from app.server import create_app
import socket
import time
import pytest


@pytest.fixture(scope="session")
def client():
    cameras_data: list[CameraData] = [{"id": 0, "type": CameraType.MOCK}]
    bus = MutiprocessingBus(cameras_data)
    notifier = MockNotification()

    start_workers(cameras_data, bus, notifier)

    app = create_app(bus)
    client = app.test_client()

    yield client  # test run here

    bus.send_terminate()


def wait_for_server(host="127.0.0.1", port=5001, timeout=5):
    start = time.time()

    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.1)

    raise RuntimeError("Server did not start in time")


def test_start(client):
    response = client.post("/cameras/0/start")
    assert response.status_code == 200


def test_stop(client):
    client.post("/cameras/0/start")
    response = client.post("/cameras/0/stop")
    assert response.status_code == 200


def test_terminate(client):
    client.post("/cameras/0/start")
    response = client.post("/cameras/terminate")
    assert response.status_code == 200
