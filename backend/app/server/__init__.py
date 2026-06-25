from flask import Flask
from flask_cors import CORS
from app.config import cors_allow_url
from app.messaging import BusInterface
from app.server.services.camera_service import CameraService
from app.server.services.storage_service import StorageServive


def create_app(bus: BusInterface, cameras_ids: list[int]):

    app = Flask(__name__)
    CORS(app, origins=cors_allow_url)

    from app.server.api.routes import bp as health_bp
    app.register_blueprint(health_bp)

    from app.server.api.api_cameras import build_cameras_bp
    camera_service = CameraService(bus, cameras_ids)
    cameras_bp = build_cameras_bp(camera_service)
    app.register_blueprint(cameras_bp)

    from app.server.api.api_storge import build_storage_bp
    storage_service = StorageServive()
    storage_bp = build_storage_bp(storage_service)
    app.register_blueprint(storage_bp)

    print("App created successfully")

    return app
