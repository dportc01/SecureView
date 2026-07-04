from flask import Flask
from flask_cors import CORS

from app.config import cors_allow_url

from app.server.services import (
    CameraService,
    StorageService,
    ConfigurationService,
    SystemService,
    LogService,
)

from app.server.api import build_storage_bp
from app.server.api import build_cameras_bp
from app.server.api import build_configuration_bp
from app.server.api import build_system_bp
from app.server.api import build_log_bp


def create_app(
    camera_service: CameraService,
    storage_service: StorageService,
    configuration_service: ConfigurationService,
    system_service: SystemService,
    log_service: LogService,
):

    app = Flask(__name__)
    CORS(app, origins=cors_allow_url)

    cameras_bp = build_cameras_bp(camera_service)
    app.register_blueprint(cameras_bp)

    storage_bp = build_storage_bp(storage_service)
    app.register_blueprint(storage_bp)

    configuration_bp = build_configuration_bp(configuration_service)
    app.register_blueprint(configuration_bp)

    system_bp = build_system_bp(camera_service, system_service)
    app.register_blueprint(system_bp)

    log_bp = build_log_bp(log_service)
    app.register_blueprint(log_bp)

    print("App created successfully")

    return app
