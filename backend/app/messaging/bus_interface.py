from typing import Protocol
from .messages import Action

class BusInterface(Protocol):

    def send_start(self, id: int) -> None:
        ...

    def send_stop(self, id: int) -> None:
        ...

    def send_terminate(self) -> None:
        ...

    def recv(self, id: int) -> Action:
        ...