from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True)
class ConfigJson:
    notification_time: int
    cameras: list[ConfigJsonCam]


@dataclass(frozen=True)
class ConfigJsonCam:
    id: int
    start_record: str
    end_record: str


@dataclass
class RecordTime:
    start: time
    end: time
