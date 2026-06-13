from app.workers.camera import factory
from app.discovery import CameraType

def test_build_mock_camera():
    camera = factory.build_camera({"type": CameraType.MOCK, "id": 0})

    camera.capture()