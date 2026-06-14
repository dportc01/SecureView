from .camera_interface import CameraInterface
from .mock_camera import MockCamera
from app.discovery import CameraData, CameraType


def build_camera(camera_data: CameraData) -> CameraInterface:
    if camera_data["type"] == CameraType.MOCK:
        return MockCamera()
    else:
        raise RuntimeError("Couldn't build camera unrecognised type")
