from flask import Blueprint, Response, jsonify
from ..services.camera_service import CameraService


def build_cameras_bp(camera_service: CameraService) -> Blueprint:

    bp = Blueprint("cameras", __name__)

    @bp.route("/cameras/<int:id>")
    def show_video(id):
        def generate_frames():
            while True:
                frame = camera_service.read_camera(id)

                if frame is None:
                    continue

                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" +
                    frame +
                    b"\r\n"
                )

        return Response(generate_frames(),
                        mimetype="multipart/x-mixed-replace; boundary=frame")

    @bp.route("/cameras/<int:id>/start", methods=["POST"])
    def start_video(id):
        res = camera_service.start_camera(id)
        return _format_response(res)

    @bp.route("/cameras/<int:id>/stop", methods=["POST"])
    def stop_video(id):
        res = camera_service.stop_camera(id)
        return _format_response(res)

    @bp.route("/cameras/terminate", methods=["POST"])
    def terminate_video():
        res = camera_service.terminate_cameras()
        return _format_response(res)

    return bp


def _format_response(res: str | None):
    if res is None:
        return jsonify({"status": "error", "message": f"Camera {id} didn't respond"}), 500

    return jsonify({"status": "ok", "message": res}), 200
