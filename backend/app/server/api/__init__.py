from .api_cameras import build_cameras_bp
from .api_configuration import build_configuration_bp
from .api_log import build_log_bp
from .api_storge import build_storage_bp
from .api_system import build_system_bp

__all__ = [
    "build_cameras_bp",
    "build_configuration_bp",
    "build_log_bp",
    "build_storage_bp",
    "build_system_bp",
]
