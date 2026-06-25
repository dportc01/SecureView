from flask import Flask
from flask_cors import CORS
from app.config import cors_allow_url
from app.messaging import BusInterface
from .services.camera_service import CameraService


def create_app(bus: BusInterface, cameras_ids: list[int]):

    app = Flask(__name__)
    CORS(app, origins=cors_allow_url)

    from .api.routes import bp as health_bp
    app.register_blueprint(health_bp)

    from .api.api_cameras import build_cameras_bp
    camera_service = CameraService(bus, cameras_ids)
    cameras_bp = build_cameras_bp(camera_service)
    app.register_blueprint(cameras_bp)

    print("App created successfully")

    return app
