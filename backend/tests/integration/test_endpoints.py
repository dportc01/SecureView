from multiprocessing import Queue
from pathlib import Path
import socket
import time
import pytest

from app.discovery import CameraData, CameraType
from app.messaging import MultiprocessingBus, BusInterface
from app.workers import start_workers, wait_and_terminate_workers
from app.notification import MockNotification
from app.server import create_app
from app.server.services import (
    CameraService,
    StorageService,
    ConfigurationService,
    SystemService,
    LogService,
)
from tests.integration.mock_recorder import MockRecorder


def make_client(record_dir: Path):
    cameras_data: list[CameraData] = [{"type": CameraType.MOCK, "id": 0}]
    bus = MultiprocessingBus(cameras_data)
    notifier = MockNotification()
    notif_queue = Queue()
    recorder = MockRecorder({"recording": False, "frame_received": False})

    record_queue = [Queue() for _ in cameras_data]

    params = start_workers(
        cameras_data=cameras_data,
        bus=bus,
        notifier=notifier,
        notif_queue=notif_queue,
        recorder=recorder,
        record_queue=record_queue,
    )

    cameras_ids = [cam["id"] for cam in cameras_data]
    system_queue = Queue()

    camera_service = CameraService(bus, cameras_ids)
    storage_service = StorageService(record_dir)
    configuration_service = ConfigurationService()
    system_service = SystemService(system_queue)
    log_service = LogService()

    app = create_app(
        camera_service=camera_service,
        storage_service=storage_service,
        configuration_service=configuration_service,
        system_service=system_service,
        log_service=log_service,
    )
    client = app.test_client()

    return (
        client,
        bus,
        params,
        notif_queue,
        record_queue,
    )


@pytest.fixture(scope="session")
def session_client(tmp_path_factory):
    record_dir = tmp_path_factory.mktemp("rectods")
    client, bus, params, notif_queue, record_queue = make_client(record_dir)

    yield client

    simulate_external_terminate(bus)
    wait_and_terminate_workers(params, notif_queue, record_queue)


@pytest.fixture(scope="function")
def function_client(tmp_path):
    client, bus, params, notif_queue, record_queue = make_client(tmp_path)

    yield client

    simulate_external_terminate(bus)
    wait_and_terminate_workers(params, notif_queue, record_queue)


def wait_for_server(host="127.0.0.1", port=5001, timeout=5):
    start = time.time()

    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.1)

    raise RuntimeError("Server did not start in time")


# ============== CAMERAS ENDPOINTS ==============
def test_start(session_client):
    response = session_client.post("/cameras/0/start")
    assert response.status_code == 200


def test_stop(session_client):
    session_client.post("/cameras/0/start")
    response = session_client.post("/cameras/0/stop")
    assert response.status_code == 200


# ============== SYSTEM ENDPOINTS ==============
def test_terminate(function_client):
    response = function_client.post("/system/terminate")
    time.sleep(0.2)
    assert response.status_code == 200


def test_restart(function_client):
    response = function_client.post("/system/restart")
    time.sleep(0.2)
    assert response.status_code == 200


# ============== STORAGE ENPOINTS ==============
def test_storage_get(function_client, tmp_path):
    file = tmp_path / "video.mp4"
    file.write_bytes(b"hello")

    response = function_client.get("/storage/get")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "video"


def test_download(function_client, tmp_path):
    file = tmp_path / "video.mp4"
    file.write_bytes(b"hello")

    response = function_client.post(
        "/storage/download",
        json={"filename": "video"},
    )

    assert response.status_code == 200
    assert response.data == b"hello"


def test_download_wrong_file(function_client, tmp_path):
    file = tmp_path / "video.mp4"
    file.write_bytes(b"hello")

    response = function_client.post(
        "/storage/download",
        json={"filename": "videa"},
    )

    assert response.status_code == 404


def test_download_no_data(session_client):
    response = session_client.post("/storage/download")
    assert response.status_code == 400


def test_delete(function_client, tmp_path):
    file = tmp_path / "video.mp4"
    file.write_bytes(b"hello")

    response = function_client.post(
        "/storage/delete",
        json={"filenames": ["video"]},
    )

    assert response.status_code == 200
    assert not file.exists()


def test_delete_wrong_file(function_client, tmp_path):
    file = tmp_path / "video.mp4"
    file.write_bytes(b"hello")

    response = function_client.post(
        "/storage/delete",
        json={"filenames": ["videa"]},
    )

    assert response.status_code == 404
    assert file.exists()


def test_delete_wrong_type(function_client, tmp_path):
    file = tmp_path / "video.mp4"
    file.write_bytes(b"hello")

    response = function_client.post(
        "/storage/delete",
        json={"filenames": "videa"},
    )

    assert response.status_code == 400


def test_delete_no_data(session_client):
    response = session_client.post("/storage/delete")
    assert response.status_code == 400


# ============== CONFIGURATIONS ENPOINTS ==============
def test_get_conf(session_client):
    respose = session_client.get("/config/get")
    assert respose.status_code == 200

    data = respose.json

    assert "notification_time" in data
    assert "cameras" in data


def simulate_external_terminate(bus: BusInterface):
    time.sleep(0.2)
    bus.send_terminate()
