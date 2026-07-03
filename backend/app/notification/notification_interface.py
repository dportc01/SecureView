from typing import Protocol


class NotificationInterface(Protocol):
    async def notify_msg(self, msg: str) -> None: ...

    async def notify_img(self, attached_msg: str, img: bytes) -> None: ...
