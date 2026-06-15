from multiprocessing import Process
import logging
from app.messaging import BusInterface
from app.discovery import CameraData
from .camera_worker import camera_woker


def start_camera_workers(cameras_data: list[CameraData], bus: BusInterface) -> list[Process]:

    if len(cameras_data) == 0:
        logging.warning("Camera data is empty")

    processes = []

    for i in range(len(cameras_data)):

        p = Process(target=camera_woker, args=(cameras_data[i], bus))
        p.start()

        processes.append(p)

    return processes


def wait_and_terminate_camera_workeres(processes: list[Process]):

    for p in processes:
        p.join()

    for p in processes:
        if p.is_alive():
            p.terminate()
            p.join()
