from flask import Blueprint, jsonify
from app.server.services.log_service import LogService


def build_log_bp(log_service: LogService) -> Blueprint:

    bp = Blueprint("log", __name__)

    @bp.route("/log/get")
    def get_log():
        log = log_service.read_log()

        if log is None:
            return {"status": "error", "message": "Couldn't open file, check "
                    "that it exist or it is readeable"}, 500

        return jsonify(log)

    return bp
