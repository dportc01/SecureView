from typing import Protocol

class BusInterface(Protocol):

    def send_start(self, id: int) -> None:
        ...

    def send_stop(self, id: int) -> None:
        ...

    def recv(self, id: int) -> None:
        ...