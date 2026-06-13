from app.discovery import CameraData
from .camera.factory import build_camera
from app.messaging import BusInterface

def camera_woker(camera_data: CameraData, bus: BusInterface):

    camera = build_camera(camera_data)

    while True:
        order = bus.recv(camera_data['id'])