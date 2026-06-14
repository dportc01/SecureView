import logging
from app.discovery import CameraData
from .camera.factory import build_camera
from app.messaging import BusInterface, Action


def camera_woker(camera_data: CameraData, bus: BusInterface):

    camera = build_camera(camera_data)
    alive = True

    while alive:
        order = bus.recv(camera_data['id'])

        if (order == Action.START):
            frame_stream = camera.start_capture()
            bus.respond_frame_stream(frame_stream)

        if (order == Action.STOP):
            camera.stop_capture()

        if (order == Action.TERMINATE):
            logging.info(f"Terminating camera {camera_data["id"]}")
            alive = False

    return
