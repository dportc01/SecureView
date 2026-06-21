from multiprocessing import Process, Queue
from threading import Thread
from queue import Full
from dataclasses import dataclass
import logging

from app.messaging import BusInterface
from app.discovery import CameraData
from app.notification import (
    NotificationInterface,
    Type as NotifType,
    Command as NotifCommand
)
from app.record import (
    Recorder,
    Type as RecType,
    Command as RecCommand
)
from app.config import MAX_QUEUE_SIZE
from .camera_worker import camera_woker
from .notification_worker import notification_worker
from .record_woker import record_woker


@dataclass
class ManagerControlParams:
    camera_processes: list[Process]
    notif_thread: Thread
    notif_queue: Queue
    record_processes: list[Process]
    record_queue: list[Queue]


def start_workers(
        cameras_data: list[CameraData],
        bus: BusInterface,
        notifier: NotificationInterface,
        recorder: Recorder) -> ManagerControlParams:

    # Notifier woker
    notif_queue = Queue(MAX_QUEUE_SIZE * len(cameras_data))
    notif_thread = notification_worker(notifier, notif_queue)

    # Camera wokers
    if len(cameras_data) == 0:
        logging.warning("Camera data is empty")

    camera_processes = []
    record_processes = []
    record_queue = []

    for i in range(len(cameras_data)):

        queue_rec = Queue()
        record_queue.append(queue_rec)
        p_rec = Process(target=record_woker, args=(recorder, queue_rec, cameras_data[i]["id"]))
        p_rec.start()
        record_processes.append(p_rec)

        p_cam = Process(target=camera_woker, args=(cameras_data[i], bus, notif_queue))
        p_cam.start()
        camera_processes.append(p_cam)

    return ManagerControlParams(
        camera_processes=camera_processes,
        notif_thread=notif_thread,
        notif_queue=notif_queue,
        record_processes=record_processes,
        record_queue=record_queue,
    )


def wait_and_terminate_workeres(control_params: ManagerControlParams):

    for p in control_params.camera_processes:
        p.join()

    _stop_notification_thread(control_params.notif_thread, control_params.notif_queue)

    _stop_record_process(control_params.record_processes, control_params.record_queue)

    # Force close everything (thread closes on return)
    for p in control_params.camera_processes:
        if p.is_alive():
            p.terminate()
            p.join()

    for p in control_params.record_processes:
        if p.is_alive():
            p.terminate()
            p.join()

    return


def _stop_notification_thread(thread: Thread, queue: Queue):
    while True:
        try:
            queue.put(NotifCommand(NotifType.TERMINATE, None, None), timeout=1)
            break
        except Full:
            pass  # retry

    thread.join()


def _stop_record_process(processes: list[Process], queue: list[Queue]):
    for q in queue:
        while True:
            try:
                q.put(RecCommand(RecType.TERMINATE, None), timeout=1)
                break
            except Full:
                pass  # retry

    for p in processes:
        p.join(timeout=10)
