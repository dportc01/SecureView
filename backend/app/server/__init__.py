from flask import Flask
from flask_cors import CORS
from app.config import cors_allow_url
from app.messaging import BusInterface
from app.server.services.camera_service import CameraService
from app.server.services.storage_service import StorageServive
from app.server.services.configuration_service import ConfigurationService
from app.server.services.system_service import SystemService
from multiprocessing import Queue


def create_app(bus: BusInterface, cameras_ids: list[int], system_queue: Queue):

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

    from app.server.api.api_configuration import build_configuration_bp
    configuration_service = ConfigurationService()
    configuration_bp = build_configuration_bp(configuration_service)
    app.register_blueprint(configuration_bp)

    from app.server.api.api_system import build_system_bp
    system_service = SystemService(system_queue)
    system_bp = build_system_bp(camera_service, system_service)
    app.register_blueprint(system_bp)

    print("App created successfully")

    return app
