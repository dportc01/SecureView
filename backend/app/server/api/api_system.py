from flask import Blueprint
from app.server.services.camera_service import CameraService
from app.server.services.system_service import SystemService


def build_system_bp(
    camera_service: CameraService, system_service: SystemService
) -> Blueprint:

    bp = Blueprint("system", __name__)

    @bp.route("/system/terminate", methods=["POST"])
    def terminate():
        success = system_service.terminate_system()
        if not success:
            return {
                "stauts": "error",
                "message": "Couldn't stop server, manual intervention required",
            }, 500

        success = camera_service.terminate_cameras()
        if success is None:
            return {
                "status": "error",
                "message": "Cameras didn't respond, " "manual intervention required",
            }, 500

        return {"status": "ok", "message": "Terminating cameras and server"}, 200

    @bp.route("/system/restart", methods=["POST"])
    def restart():
        success = system_service.restart_system()
        if not success:
            return {
                "status": "error",
                "message": "Couldn't restart server, manual intervention required",
            }, 500

        success = camera_service.terminate_cameras()
        if success is None:
            return {
                "status": "error",
                "message": "Cameras didn't respond, " "manual intervention required",
            }, 500

        return {"status": "ok", "message": "Restarting cameras and server"}, 200

    return bp
