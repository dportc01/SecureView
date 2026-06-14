from .camera_interface import CameraInterface
from .mock_camera import MockCamera
from .local_camera import LocalCamera
from app.discovery import CameraData, CameraType


def build_camera(camera_data: CameraData) -> CameraInterface:
    if camera_data["type"] == CameraType.MOCK:
        return MockCamera()
    if camera_data["type"] == CameraType.LOCAL:
        return LocalCamera(device_index=camera_data["id"])
    else:
        raise RuntimeError("Couldn't build camera unrecognised type")
