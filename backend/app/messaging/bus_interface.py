from typing import Protocol
from .messages import Action


class BusInterface(Protocol):

    def send_start(self, id: int) -> None:
        ...

    def send_stop(self, id: int) -> None:
        ...

    def send_terminate(self) -> None:
        ...

    # TODO: Change name this should be more verbose and reflect that it is the camera,
    # the one that it is recving on this case
    def recv(self, id: int) -> Action:
        ...

    def write_frame(self, id: int, frame: bytes) -> None:
        ...

    def read_frame(self, id: int) -> bytes:
        ...

    def respond(self, response: str) -> None:
        ...

    def read_response(self) -> str:
        ...
