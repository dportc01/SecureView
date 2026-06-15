from flask import Flask
from app.messaging import BusInterface
from .services.camera_service import CameraService


def create_app(bus: BusInterface):

    app = Flask(__name__)

    from .api.routes import bp as health_bp
    app.register_blueprint(health_bp)

    from .api.api_cameras import build_cameras_bp
    camera_service = CameraService(bus)
    cameras_bp = build_cameras_bp(camera_service)
    app.register_blueprint(cameras_bp)

    print("App created successfully")

    return app
