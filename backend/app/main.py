from .server import create_app
from .discovery import discover_cameras
from .workers import start_camera_workers
from .messaging import MutiprocessingBus


if __name__ == "__main__":

    cameras_data = discover_cameras()

    print(cameras_data)

    bus = MutiprocessingBus(cameras_data)

    start_camera_workers(cameras_data, bus)

    bus.send_start(0)
    bus.send_start(2)

    app = create_app(bus)
    app.run(host="0.0.0.0", port=5000)
