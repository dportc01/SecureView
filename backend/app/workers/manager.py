from multiprocessing import Process, Queue
from queue import Full
from dataclasses import dataclass
import logging

from threading import Thread
from app.messaging import BusInterface
from app.discovery import CameraData
from app.notification import NotificationInterface, Command, Type
# from app.record import Recorder
from app.config import MAX_QUEUE_SIZE
from .camera_worker import camera_woker
from .notification_worker import notification_worker
# from .record_woker import record_woker


@dataclass
class ManagerControlParams:
    camera_processes: list[Process]
    notif_thread: Thread
    notif_queue: Queue
    # worker_processes: list[Process]


def start_workers(
        cameras_data: list[CameraData],
        bus: BusInterface,
        notifier: NotificationInterface,
        ) -> ManagerControlParams:

    # Notifier woker
    notif_queue = Queue(MAX_QUEUE_SIZE * len(cameras_data))
    notif_thread = notification_worker(notifier, notif_queue)

    # Camera wokers
    if len(cameras_data) == 0:
        logging.warning("Camera data is empty")

    camera_processes = []
    worker_processes = []

    for i in range(len(cameras_data)):

        # queue_rec = Queue()
        # p_rec = Process(target=record_woker, args=(recorder, queue_rec, cameras_data[i]["id"]))

        p_cam = Process(target=camera_woker, args=(cameras_data[i], bus, notif_queue))
        p_cam.start()

        camera_processes.append(p_cam)

    return ManagerControlParams(
        camera_processes=camera_processes,
        notif_thread=notif_thread,
        notif_queue=notif_queue,
        # worker_processes=worker_processes,
    )


def wait_and_terminate_workeres(control_params: ManagerControlParams):

    for p in control_params.camera_processes:
        p.join()

    # When camera_wokers stop cleanup notifications
    while True:
        try:
            control_params.notif_queue.put(Command(Type.TERMINATE, None, None), timeout=1)
            break
        except Full:
            pass  # retry

    control_params.notif_thread.join()

    for p in control_params.camera_processes:
        if p.is_alive():
            p.terminate()
            p.join()

    return
