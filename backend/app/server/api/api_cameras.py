from flask import Blueprint, Response, jsonify
from app.server.services.camera_service import CameraService


def build_cameras_bp(camera_service: CameraService) -> Blueprint:

    bp = Blueprint("cameras", __name__)

    @bp.route("/cameras/discover")
    def discover_cameras():
        ids = camera_service.get_disovered_cameras()
        res = jsonify(ids)
        return res, 200

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
        return _format_response(res, id)

    @bp.route("/cameras/<int:id>/stop", methods=["POST"])
    def stop_video(id):
        res = camera_service.stop_camera(id)
        return _format_response(res, id)

    return bp


def _format_response(res: str | None, id: int):
    if res is None:
        return {"status": "error", "message": f"Camera {id} didn't respond"}, 500

    return {"status": "ok", "message": res}, 200
