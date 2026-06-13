from backend.app.workers.camera_interface import CameraInterface


class CameraService:
    def __init__(self, camera: CameraInterface):
        self.camera = camera

    def get_available_cameras(self):
        return self.camera.get_camera_count()
