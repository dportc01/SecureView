from flask import Blueprint, Response


def build_cameras_bp(camera_service) -> Blueprint:

    bp = Blueprint("cameras", __name__)

    @bp.route("/video/<int:id>")
    def video(id):
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

    return bp
