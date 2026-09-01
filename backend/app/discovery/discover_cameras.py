from typing import TypedDict
from enum import Enum
import cv2
import platform

import app.config as config


class CameraType(Enum):
    MOCK = "MOCK"
    LOCAL = "LOCAL"


class CameraData(TypedDict):
    type: CameraType
    id: int


def discover_cameras() -> list[CameraData]:

    cameras_data: list[CameraData] = []
    system = platform.system()

    module = cv2.CAP_ANY

    if system == "Linux":
        module = cv2.CAP_V4L2
    elif system == "Windows":
        module = cv2.CAP_DSHOW

    try:
        max_camera_index = int(config.MAX_LOCAL_CAMERA_INDEX) + 1
    except (TypeError, ValueError):
        raise ValueError("MAX_LOCAL_CAMERA_INDEX must be a number")

    if max_camera_index <= 0:
        raise ValueError("MAX_LOCAL_CAMERA_INDEX must be 0 or greater")

    for i in range(max_camera_index):
        cap = cv2.VideoCapture(i, module)
        if cap.isOpened():
            cap.release()
            cameras_data.append({"id": i, "type": CameraType.LOCAL})

    return cameras_data
