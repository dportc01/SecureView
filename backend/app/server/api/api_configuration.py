from flask import Blueprint, jsonify
from app.server.services.configuration_service import ConfigurationService


def build_configuration_bp(configuration_service: ConfigurationService) -> Blueprint:

    bp = Blueprint("configuration", __name__)

    @bp.route("/config/get")
    def get_config():
        conf = configuration_service.get_configuration()

        return jsonify(conf), 200

    return bp
