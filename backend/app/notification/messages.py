from dataclasses import dataclass
from enum import Enum


@dataclass
class Command:
    type: Type
    msg: str | None
    img: bytes | None


class Type(str, Enum):
    MESSAGE = "MESSAGE"
    IMAGE = "IMAGE"
    TERMINATE = "TERMINATE"
