from dataclasses import dataclass
from enum import Enum


@dataclass
class Command:
    type: Type
    frame: bytes


class Type(str, Enum):
    FRAME = "FRAME"
