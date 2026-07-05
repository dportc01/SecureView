from multiprocessing import Queue
from pathlib import Path
import socket
import time
import pytest
import json

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
from app.config.config_types import ConfigJson, ConfigJsonCam
from tests.integration.mock_recorder import MockRecorder


def make_client(record_dir: Path, log_path: Path, config_path: Path):
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
    configuration_service = ConfigurationService(
        config_path,
        ConfigJson(
            notification_time=10,
            cameras=[
                ConfigJsonCam(id=0, start_record="08:00", end_record="22:00"),
                ConfigJsonCam(id=2, start_record="12:00", end_record="19:00"),
            ],
        ),
    )
    system_service = SystemService(system_queue)
    log_service = LogService(log_path)

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
    record_dir = tmp_path_factory.mktemp("records")
    log_path = tmp_path_factory.mktemp("logs") / "app.log"
    config_path = tmp_path_factory.mktemp("config") / "config.json"
    client, bus, params, notif_queue, record_queue = make_client(
        record_dir, log_path, config_path
    )

    yield client

    simulate_external_terminate(bus)
    wait_and_terminate_workers(params, notif_queue, record_queue)


@pytest.fixture(scope="function")
def function_client(tmp_path):
    log_path = tmp_path / "app.log"
    config_path = tmp_path / "config.json"
    client, bus, params, notif_queue, record_queue = make_client(
        tmp_path, log_path, config_path
    )

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
def test_discover(session_client):
    response = session_client.get("/cameras/discover")
    data = response.json

    assert response.status_code == 200
    assert data is not None


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
    assert response.status_code == 200


def test_restart(function_client):
    response = function_client.post("/system/restart")
    assert response.status_code == 200


# ============== STORAGE ENPOINTS ==============
def test_storage_get(function_client, tmp_path):
    file = tmp_path / "video.mp4"
    file.touch()

    file_thrash = tmp_path / "Trash.txt"
    file_thrash.touch()

    response = function_client.get("/storage/get")
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1
    assert data[0]["name"] == "video"


def test_download(function_client, tmp_path):
    file = tmp_path / "video.mp4"
    file.write_text("hello", encoding="utf-8")

    response = function_client.post(
        "/storage/download",
        json={"filename": "video"},
    )

    assert response.status_code == 200
    assert response.data == b"hello"


def test_download_wrong_file(function_client, tmp_path):
    file = tmp_path / "video.mp4"
    file.touch()

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
    file.touch()

    response = function_client.post(
        "/storage/delete",
        json={"filenames": ["video"]},
    )

    assert response.status_code == 200
    assert not file.exists()


def test_delete_wrong_file(function_client, tmp_path):
    file = tmp_path / "video.mp4"
    file.touch()

    response = function_client.post(
        "/storage/delete",
        json={"filenames": ["videa"]},
    )

    assert response.status_code == 404
    assert file.exists()


def test_delete_wrong_type(function_client, tmp_path):
    file = tmp_path / "video.mp4"
    file.touch()

    response = function_client.post(
        "/storage/delete",
        json={"filenames": "video"},
    )

    assert response.status_code == 400


def test_delete_no_data(session_client):
    response = session_client.post("/storage/delete")
    assert response.status_code == 400


# ============== CONFIGURATIONS ENPOINTS ==============
def test_get_conf(session_client):
    expected = {
        "cameras": [
            {
                "id": 0,
                "start_record": "08:00",
                "end_record": "22:00",
            },
            {
                "id": 2,
                "start_record": "12:00",
                "end_record": "19:00",
            },
        ],
        "notification_time": 10,
    }

    respose = session_client.get("/config/get")

    assert respose.status_code == 200
    assert respose.get_json() == expected


def test_update_conf(function_client, tmp_path):
    expected = {
        "cameras": [
            {
                "id": 1,
                "start_record": "00:00",
                "end_record": "06:00",
            },
        ],
        "notification_time": 60,
    }
    file = tmp_path / "config.json"

    response = function_client.put("/config/update", json=expected)

    assert response.status_code == 200
    assert json.loads(file.read_text()) == expected


def test_update_conf_no_data(session_client):
    response = session_client.put("/config/update")

    assert response.status_code == 400


# ============== LOG ENPOINTS ==============
def test_get_log(function_client, tmp_path):
    file = tmp_path / "app.log"
    file.write_text(
        "TIME: 2026-07-05 12:45:15,613 - LEVEL: INFO - CAMERA:0 - MESSAGE: Opening camera",
        encoding="utf-8",
    )

    file_trash = tmp_path / "video.mp4"
    file_trash.touch()

    response = function_client.get("/log/get")
    logs = response.json["logs"]

    assert response.status_code == 200
    assert len(logs) == 1
    assert logs[0]["level"] == "INFO"
    assert logs[0]["source"] == "CAMERA:0"
    assert logs[0]["time"] == "2026-07-05 12:45:15,613"
    assert logs[0]["message"] == "Opening camera"


def test_get_log_no_file(function_client):
    response = function_client.get("/log/get")
    assert response.status_code == 500


def test_clean_log(function_client, tmp_path):
    file = tmp_path / "app.log"
    file.write_text(
        "TIME: 2026-07-05 12:45:15,613 - LEVEL: INFO - CAMERA:0 - MESSAGE: Opening camera",
        encoding="utf-8",
    )

    response = function_client.put("/log/clean")

    assert response.status_code == 200
    assert file.exists()
    assert file.read_text() == ""


def test_donwload_log(function_client, tmp_path):
    file = tmp_path / "app.log"
    file.write_text(
        "TIME: 2026-07-05 12:45:15,613 - LEVEL: INFO - CAMERA:0 - MESSAGE: Opening camera",
        encoding="utf-8",
    )

    response = function_client.get("/log/download")

    assert response.status_code == 200
    assert (
        response.data
        == b"TIME: 2026-07-05 12:45:15,613 - LEVEL: INFO - CAMERA:0 - MESSAGE: Opening camera"
    )


def test_donwload_log_no_file(function_client):
    response = function_client.get("/log/download")
    assert response.status_code == 404


def simulate_external_terminate(bus: BusInterface):
    time.sleep(0.2)
    bus.send_terminate()
