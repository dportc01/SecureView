from typing import Protocol


class NotificationInterface(Protocol):
    def start(self):
        ...

    def notify(self, msg: str):
        ...
