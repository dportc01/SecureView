from backend.app.workers.camera.camera_interface import CameraInterface


class CameraService:
    def __init__(self, camera: CameraInterface):
        self.camera = camera
