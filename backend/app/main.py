import time
from waitress import serve
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
from .discovery import discover_cameras, CameraData
from .workers import start_workers, wait_and_terminate_workers
from .messaging import MultiprocessingBus, BusInterface
from .notification import TelegramNotification
from .record import Recorder
from .config import (
    MAX_QUEUE_SIZE,
    MAX_FRAME_QUEUE_SIZE,
    RECORD_DIR,
    LOG_PATH,
    CONFIG_JSON_PATH,
    CONF_JSON,
    SERVER_PORT,
    SERVER_THREADS,
)
from .logging.loggers import get_system_logger


def _run_server(bus: BusInterface, cameras_ids: list[int], system_queue: Queue):
    camera_service = CameraService(bus, cameras_ids)
    storage_service = StorageService(Path(RECORD_DIR))
    configuration_service = ConfigurationService(CONFIG_JSON_PATH, CONF_JSON)
    system_service = SystemService(system_queue)
    log_service = LogService(Path(LOG_PATH))

    server = create_app(
        camera_service=camera_service,
        storage_service=storage_service,
        configuration_service=configuration_service,
        system_service=system_service,
        log_service=log_service,
    )

    serve(
        server,
        host="0.0.0.0",
        port=SERVER_PORT,
        threads=SERVER_THREADS,
    )


def _run_workers(
    bus: BusInterface,
    recorder_queue: list[Queue],
    notif_queue: Queue,
    cameras_data: list[CameraData],
):
    # Initialize everything, queues need to be initialized on __main__
    notifier = TelegramNotification()
    recorder = Recorder(Path(RECORD_DIR))
    for _ in range(len(cameras_data)):
        recorder_queue.append(Queue(MAX_FRAME_QUEUE_SIZE))

    return start_workers(
        cameras_data=cameras_data,
        bus=bus,
        notifier=notifier,
        notif_queue=notif_queue,
        recorder=recorder,
        record_queue=recorder_queue,
    )


def start_all() -> bool:
    # Initialize everything, queues need to be initialized on __main__
    cameras_data = discover_cameras()
    bus = MultiprocessingBus(cameras_data)
    notif_queue = Queue(MAX_QUEUE_SIZE * len(cameras_data))
    recorder_queue = []
    processes = _run_workers(bus, recorder_queue, notif_queue, cameras_data)

    cameras_ids = [cam["id"] for cam in cameras_data]

    system_queue = Queue()
    # Server is run from a process instead of a thread to better handle termination
    app_process = Process(target=_run_server, args=(bus, cameras_ids, system_queue))
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
