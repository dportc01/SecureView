import logging
import time
from app.discovery import CameraData
from app.camera.factory import build_camera
from app.messaging import BusInterface, Action


# TODO: If camera is alredy stopped change the respond message
def camera_woker(camera_data: CameraData, bus: BusInterface):

    camera = build_camera(camera_data)
    alive = True

    while alive:
        order = bus.cam_recv(camera_data['id'])

        if (order == Action.START):
            bus.respond(f"Starting recording on camera: {camera_data['id']}")
            frame_stream = camera.start_capture()
            for frame in frame_stream:
                bus.write_frame(camera_data['id'], frame.to_bytes())

                order = bus.cam_recv(camera_data['id'])
                if order == Action.STOP or order == Action.TERMINATE:
                    frame_stream = None  # Maybe unnecesary
                    break

        if (order == Action.STOP):
            bus.respond(f"Stoping recording on camera: {camera_data['id']}")
            camera.stop_capture()

        if (order == Action.TERMINATE):
            bus.respond(f"Terminating camera: {camera_data['id']}")
            logging.info(f"Terminating camera {camera_data['id']}")
            alive = False
            print("terminated")

    time.sleep(0.1)  # Wait time to complete response operations, could make terminate not respond
    bus.close()
    return
