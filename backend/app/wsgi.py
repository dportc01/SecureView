from app.server import create_app
from app.messaging import MutiprocessingBus
from .discovery import discover_cameras

cameras_data = discover_cameras()

bus = MutiprocessingBus(cameras_data)

app = create_app(bus)
