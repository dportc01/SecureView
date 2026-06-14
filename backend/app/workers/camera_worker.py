import logging
from app.discovery import CameraData
from .camera.factory import build_camera
from app.messaging import BusInterface, Action

def camera_woker(camera_data: CameraData, bus: BusInterface):

    camera = build_camera(camera_data)
    alive = True

    while alive:
        order = bus.recv(camera_data['id'])

        if (order == Action.TERMINATE):
            logging.info(f"Terminating camera {camera_data["id"]}")
            alive = False

    return
