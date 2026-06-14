from app.workers.camera import factory
from app.discovery import CameraType
from app.workers.camera.mock_camera import MockCamera
from app.workers.camera.local_camera import LocalCamera


def test_build_mock_camera():
    camera = factory.build_camera({"type": CameraType.MOCK, "id": 0})

    assert isinstance(camera, MockCamera)

def test_build_local_camera():
    camera = factory.build_camera({"type": CameraType.LOCAL, "id": 0})

    assert isinstance(camera, LocalCamera)