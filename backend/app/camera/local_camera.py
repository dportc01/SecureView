import cv2
import platform
from typing import Iterable
from app.logging.loggers import get_camera_logger
from .frame import Frame


class LocalCamera:
    def __init__(self, device_index):
        self.device_index = device_index
        self.cap = None
        self.module = cv2.CAP_ANY
        self.logger = get_camera_logger(self.device_index)

        system = platform.system()
        if system == "Linux":
            self.module = cv2.CAP_V4L2
        elif system == "Windows":
            self.module = cv2.CAP_DSHOW

    def open_camera(self) -> None:
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.device_index, self.module)

            if not self.cap.isOpened():
                self.cap.release()
                self.cap = None
                raise RuntimeError(f"Failed to open camera: {self.device_index}")

            self.logger.info("Opening camera")
        else:
            self.logger.warning("Alredy capturing")
            return

    def start_capture(self) -> Iterable[Frame]:
        if self.cap is None:
            self.logger.error("Camera is not opened")
        else:
            self.logger.info("Starting camera capture")
            try:
                while True:
                    success, frame = self.cap.read()

                    if not success:
                        break

                    height, width = frame.shape[:2]

                    yield Frame(
                        data=frame,
                        width=width,
                        height=height,
                    )
            except Exception as e:
                self.logger.exception(f"Sudden stop {e}")
                self.stop_camera()

    def stop_camera(self) -> None:
        if self.cap is None:
            self.logger.warning("Tried to stop incative camera")
        else:
            self.logger.info("Stopped video capture")
            self.cap.release()
            self.cap = None
