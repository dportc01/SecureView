from multiprocessing import Process
from app.messaging import BusInterface
from app.discovery import CameraData
from .camera_worker import camera_woker

def start_camera_workers(cameras_data: list[CameraData], bus: BusInterface):


    for i in range(len(cameras_data)):

        p = Process(target=camera_woker, args=(cameras_data[i], bus))
