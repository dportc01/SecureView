import time
from multiprocessing import Queue, Process
from queue import Empty
from pathlib import Path

from .server import create_app
from .server.services import (
    CameraService,
    StorageService,
    ConfigurationService,
    SystemService,
    LogService,
)
from .discovery import discover_cameras
from .workers import start_workers, wait_and_terminate_workers
from .messaging import MultiprocessingBus, BusInterface
from .notification import TelegramNotification
from .record import Recorder
from .config import MAX_QUEUE_SIZE, MAX_FRAME_QUEUE_SIZE, RECORD_DIR
from .logging.loggers import get_system_logger


def run_app(bus: BusInterface, cameras_ids: list[int], system_queue: Queue):
    print(f"PATH: {RECORD_DIR}")
    camera_service = CameraService(bus, cameras_ids)
    storage_service = StorageService(Path(RECORD_DIR))
    configuration_service = ConfigurationService()
    system_service = SystemService(system_queue)
    log_service = LogService()
    app = create_app(
        camera_service=camera_service,
        storage_service=storage_service,
        configuration_service=configuration_service,
        system_service=system_service,
        log_service=log_service,
    )
    app.run(host="0.0.0.0", port=5000)


def start_all() -> bool:
    # Initialize everything, queues need to be initialized on __main__
    cameras_data = discover_cameras()
    bus = MultiprocessingBus(cameras_data)
    notifier = TelegramNotification()
    notif_queue = Queue(MAX_QUEUE_SIZE * len(cameras_data))
    recorder = Recorder()
    recorder_queue = []
    for _ in range(len(cameras_data)):
        recorder_queue.append(Queue(MAX_FRAME_QUEUE_SIZE))

    processes = start_workers(
        cameras_data=cameras_data,
        bus=bus,
        notifier=notifier,
        notif_queue=notif_queue,
        recorder=recorder,
        record_queue=recorder_queue,
    )

    cameras_ids = [cam["id"] for cam in cameras_data]

    system_queue = Queue()
    # Server is run from a process instead of a thread to better handle termination
    app_process = Process(target=run_app, args=(bus, cameras_ids, system_queue))
    app_process.start()

    wait_and_terminate_workers(processes, notif_queue, recorder_queue)

    try:
        restart = system_queue.get(timeout=5)
        # Clear queue
        while True:
            try:
                system_queue.get_nowait()
            except Empty:
                break
    except Empty:
        restart = False

    time.sleep(0.5)  # Wait for Flask request to completly send
    app_process.terminate()
    app_process.join()

    return restart


if __name__ == "__main__":
    logger = get_system_logger()

    while True:
        restart = start_all()

        if restart:
            # Maybe change for log on the future
            print("================ Restarting system ================")
            logger.info("Restarting system")
        else:
            print("================ Terminating system ================")
            logger.info("Terminating system")
            break
