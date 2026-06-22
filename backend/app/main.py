from .server import create_app
from .discovery import discover_cameras
from .workers import start_workers
from .messaging import MultiprocessingBus
from .notification import TelegramNotification
from .record import Recorder
from .config import MAX_QUEUE_SIZE, MAX_FRAME_QUEUE_SIZE
from multiprocessing import Queue


if __name__ == "__main__":

    # Initialize everything, queues need to be initialized on __main__
    cameras_data = discover_cameras()
    bus = MultiprocessingBus(cameras_data)
    notifier = TelegramNotification()
    notif_queue = Queue(MAX_QUEUE_SIZE * len(cameras_data))
    recorder = Recorder()
    recorder_queue = []
    for _ in range(len(cameras_data)):
        recorder_queue.append(Queue(MAX_FRAME_QUEUE_SIZE))

    start_workers(
        cameras_data=cameras_data,
        bus=bus,
        notifier=notifier,
        notif_queue=notif_queue,
        recorder=recorder,
        record_queue=recorder_queue
    )

    app = create_app(bus)
    app.run(host="0.0.0.0", port=5000)
