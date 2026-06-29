from flask import Blueprint, jsonify, request
from app.server.services.configuration_service import ConfigurationService


def build_configuration_bp(configuration_service: ConfigurationService) -> Blueprint:

    bp = Blueprint("configuration", __name__)

    @bp.route("/config/get")
    def get_config():
        conf = configuration_service.get_configuration()

        return jsonify(conf), 200

    @bp.route("/config/update", methods=["PUT"])
    def update_config():
        data = request.get_json(silent=True)
        if not data:
            return {"status": "error", "message": "Missing fields on request"}, 400

        success = configuration_service.update_configuration(data)
        if not success:
            return {"status": "error", "message": "Couldn't update file"}, 500
        return {"status": "ok", "message": "Successfully updated config"}, 200

    return bp
