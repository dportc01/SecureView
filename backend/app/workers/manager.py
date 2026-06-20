from multiprocessing import Process, Queue
from dataclasses import dataclass
import logging

from threading import Thread
from app.messaging import BusInterface
from app.discovery import CameraData
from app.notification import NotificationInterface, Command, Type
from app.config import MAX_QUEUE_SIZE
from .camera_worker import camera_woker
from .notification_worker import notification_worker


@dataclass
class ManagerControlParams:
    camera_processes: list[Process]
    notif_thread: Thread
    notif_queue: Queue


def start_workers(
        cameras_data: list[CameraData],
        bus: BusInterface,
        notifier: NotificationInterface) -> ManagerControlParams:

    # Notifier woker
    notif_queue = Queue(MAX_QUEUE_SIZE * len(cameras_data))
    notif_thread = notification_worker(notifier, notif_queue)

    # Camera wokers
    if len(cameras_data) == 0:
        logging.warning("Camera data is empty")

    processes = []

    for i in range(len(cameras_data)):

        p = Process(target=camera_woker, args=(cameras_data[i], bus, notif_queue))
        p.start()

        processes.append(p)

    return ManagerControlParams(
        camera_processes=processes,
        notif_thread=notif_thread,
        notif_queue=notif_queue
    )


def wait_and_terminate_workeres(control_params: ManagerControlParams):

    for p in control_params.camera_processes:
        p.join()

    # When camera_wokers stop cleanup everything
    control_params.notif_queue.put_nowait(Command(Type.TERMINATE, None, None))
    control_params.notif_thread.join()

    for p in control_params.camera_processes:
        if p.is_alive():
            p.terminate()
            p.join()

    return
