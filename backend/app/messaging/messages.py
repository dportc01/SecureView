from dataclasses import dataclass
from enum import Enum


@dataclass
class Command:
    dev_id: int
    action: Action


class Action(Enum):
    START = "START"
    STOP = "STOP"
    TERMINATE = "TERMINATE"
