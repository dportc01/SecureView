from dataclasses import dataclass
from enum import Enum


@dataclass
class Command:
    dev_id: int
    action: Action


class Action(str, Enum):
    START = "START"
    STOP = "STOP"
    TERMINATE = "TERMINATE"
