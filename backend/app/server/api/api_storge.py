from flask import Blueprint, jsonify
from app.server.services.storage_service import StorageServive


def build_storage_bp(storage_service: StorageServive) -> Blueprint:
    bp = Blueprint("storage", __name__)

    @bp.route("/storage/get")
    def get_storage():
        files = storage_service.get_records()
        return jsonify(files), 200

    return bp
