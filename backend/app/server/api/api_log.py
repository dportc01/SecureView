from flask import Blueprint, jsonify, send_file

from app.server.services import LogService


def build_log_bp(log_service: LogService) -> Blueprint:

    bp = Blueprint("log", __name__)

    @bp.route("/log/get")
    def get_log():
        log = log_service.read_log()

        if log is None:
            return {
                "status": "error",
                "message": "Couldn't open file, check "
                "that it exist or it is readeable",
            }, 500

        size = log_service.log_size()

        res = {"logs": log, "size": size}

        return jsonify(res)

    @bp.route("/log/clean", methods=["PUT"])
    def clean_log():
        success = log_service.clean_log()

        if not success:
            return {
                "status": "error",
                "message": "Couldn't delete the contents of the file",
            }, 500

        return {"status": "ok", "message": "Succesfully deleted app.log contents"}, 200

    @bp.route("/log/download")
    def download_log():
        return send_file(
            log_service.log_path,
            as_attachment=True,
            download_name="app.log",
            mimetype="text/plain",
        )

    return bp
