from .server import create_app
from .discovery import discover_cameras
from .workers import start_camera_workers
from .messaging import MutiprocessingBus


if __name__ == "__main__":

    cameras_data = discover_cameras()

    bus = MutiprocessingBus(cameras_data)

    start_camera_workers(cameras_data, bus)

    app = create_app(bus)
    app.run(host="0.0.0.0", port=5000)
