from app.server import create_app
from app.messaging import MutiprocessingBus

bus = MutiprocessingBus(0)

app = create_app(bus)
