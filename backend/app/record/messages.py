from dataclasses import dataclass
from enum import Enum
import numpy as np


@dataclass
class Command:
    type: Type
    frame: np.ndarray | None


class Type(Enum):
    STOP = "STOP"
    FRAME = "FRAME"
    TERMINATE = "TERMINATE"  # Only meant to be called by manager
