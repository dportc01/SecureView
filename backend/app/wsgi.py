from app.server import create_app
from app.messaging import MultiprocessingBus
from .discovery import discover_cameras

cameras_data = discover_cameras()

bus = MultiprocessingBus(cameras_data)

cameras_ids = [cam["id"] for cam in cameras_data]
app = create_app(bus, cameras_ids)
