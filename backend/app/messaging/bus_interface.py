from typing import Protocol, Iterable
from .messages import Action


class BusInterface(Protocol):

    def send_start(self, id: int) -> None:
        ...

    def send_stop(self, id: int) -> None:
        ...

    def send_terminate(self) -> None:
        ...

    #TODO: Change name to recieve this should be more verbose and
    # reflect that it is the camera, the one that it is recving on
    # this case
    def recv(self, id: int) -> Action:
        ...

    def respond_frame_stream(self, frame_stream: Iterable[bytes]) -> None:
        ...

    def read_frame_stream(self) -> None:
        ...

    def respond(self, response: str) -> None:
        ...
