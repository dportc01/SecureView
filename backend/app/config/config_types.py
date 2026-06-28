from dataclasses import dataclass
from datetime import time


@dataclass
class ConfigJson:
    notification_time: int
    cameras: list[ConfigJsonTime]


@dataclass
class ConfigJsonTime:
    id: int
    start_record: str
    end_record: str


@dataclass
class RecordTime:
    start: time
    end: time
