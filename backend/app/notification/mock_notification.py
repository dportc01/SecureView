class MockNotification():
    async def notify_msg(self, msg: str) -> None:
        print("Mock message notification")

    async def notify_img(self, attached_msg: str, img: bytes) -> None:
        print("Mock image notification")
