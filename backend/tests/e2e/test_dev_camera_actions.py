from app.server import create_app
from app.discovery import CameraData, CameraType
from app.messaging import MutiprocessingBus, BusInterface
from app.workers import start_camera_workers
from multiprocessing import Process
import requests
import socket
import time
import pytest


@pytest.fixture(scope="session")
def server():
    cameras_data: list[CameraData] = [{"id": 0, "type": CameraType.MOCK}]
    bus = MutiprocessingBus(cameras_data)

    p = Process(target=start_server, args=(bus, cameras_data))
    p.start()

    wait_for_server()

    yield  # test run here

    bus.send_terminate()
    time.sleep(0.1)

    p.terminate()
    p.join()


def start_server(bus: BusInterface, cameras_data: list[CameraData]):

    start_camera_workers(cameras_data, bus)

    app = create_app(bus)
    app.run(host="0.0.0.0", port=5001, debug=False, use_reloader=False)

    return app


def wait_for_server(host="127.0.0.1", port=5001, timeout=5):
    start = time.time()

    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.1)

    raise RuntimeError("Server did not start in time")


def test_start(server):
    response = requests.post("http://127.0.0.1:5001/cameras/0/start")
    assert response.status_code == 200


def test_stop(server):
    requests.post("http://127.0.0.1:5001/cameras/0/start")
    response = requests.post("http://127.0.0.1:5001/cameras/0/stop")
    assert response.status_code == 200


def test_terminate(server):
    requests.post("http://127.0.0.1:5001/cameras/0/start")
    response = requests.post("http://127.0.0.1:5001/cameras/terminate")
    assert response.status_code == 200
