class MockNotification():
    def __init__(self) -> None:
        self.msg_called = False
        self.img_called = False

    async def notify_msg(self, msg: str) -> None:
        self.msg_called = True
        print("Mock message notification")

    async def notify_img(self, attached_msg: str, img: bytes) -> None:
        self.img_called = True
        print("Mock image notification")
