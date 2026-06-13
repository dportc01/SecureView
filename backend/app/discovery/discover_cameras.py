from typing import TypedDict
from enum import Enum


class CameraType(str, Enum):
    MOCK = "MOCK"

class CameraData(TypedDict):
    type: CameraType
    id: int