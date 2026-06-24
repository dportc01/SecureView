from app.discovery import CameraData, CameraType
from app.messaging import MultiprocessingBus, BusInterface
from app.workers import start_workers, wait_and_terminate_workeres
from app.notification import MockNotification
from app.server import create_app
from tests.integration.recorder_mock import RecorderMock
from multiprocessing import Queue
import socket
import time
import pytest
import logging


@pytest.fixture(scope="session")
def client():
    cameras_data: list[CameraData] = [{"type": CameraType.MOCK, "id": 0}]
    bus = MultiprocessingBus(cameras_data)
    notifier = MockNotification()
    notif_queue = Queue()
    recorder = RecorderMock({
        "recording": False,
        "frame_received": False
    })
    record_queue = []
    for _ in range(len(cameras_data)):
        record_queue.append(Queue())

    params = start_workers(
        cameras_data=cameras_data,
        bus=bus,
        notifier=notifier,
        notif_queue=notif_queue,
        recorder=recorder,
        record_queue=record_queue
    )

    cameras_ids = [cam["id"] for cam in cameras_data]
    app = create_app(bus, cameras_ids)
    client = app.test_client()

    yield client  # test run here

    simulate_external_terminate(bus)
    wait_and_terminate_workeres(params, notif_queue, record_queue)


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


def simulate_external_terminate(bus: BusInterface):
    time.sleep(0.2)
    logging.warning("Attempt termination:")
    bus.send_terminate()
