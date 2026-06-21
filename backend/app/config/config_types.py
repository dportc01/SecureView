from dataclasses import dataclass
from datetime import time


@dataclass
class RecordTime:
    start: time
    end: time
