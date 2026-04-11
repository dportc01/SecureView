from app.services.camera_service import CameraService
from app.mock.camera_mock import CameraMock

def test_get_cameras():
    camera = CameraMock()
    service = CameraService(camera)
    assert service.get_available_cameras() >= 1