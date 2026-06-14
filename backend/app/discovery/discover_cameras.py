from typing import TypedDict
from enum import Enum
import cv2
import platform
import app.config as config


class CameraType(str, Enum):
    MOCK = "MOCK"
    LOCAL = "LOCAL"


class CameraData(TypedDict):
    type: CameraType
    id: int


def discover_camereas() -> list[CameraData]:

    cameras_data: list[CameraData] = []
    system = platform.system()

    # Module spcification helps supress not found camera related issues.
    # To completly silence warnign set MAX_LOCAL_CAMERA_INDEX to the number
    # of cameras
    module = cv2.CAP_ANY

    if (system == "Linux"):
        module = cv2.CAP_V4L2
    elif (system == "Windows"):
        module = cv2.CAP_DSHOW

    for i in range(config.MAX_LOCAL_CAMERA_INDEX):
        cap = cv2.VideoCapture(i, module)
        if cap.isOpened():
            cap.release()
            cameras_data.append({"id": i, "type": CameraType.LOCAL})

    return cameras_data
