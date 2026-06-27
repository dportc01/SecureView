from flask import Blueprint, jsonify, request, Response
from app.server.services.storage_service import StorageServive


def build_storage_bp(storage_service: StorageServive) -> Blueprint:
    bp = Blueprint("storage", __name__)

    @bp.route("/storage/get")
    def get_storage():
        files = storage_service.get_records()
        return jsonify(files), 200

    @bp.route("/storage/download", methods=["POST"])
    def download_file():
        data = request.get_json(silent=True)

        if not data or "filename" not in data:
            return {"status": "error", "message": 'Missing "filename" on request'}, 400

        file = storage_service.get_file(data["filename"])

        if file is None:
            return {"status": "error", "message": "File not found"}, 404

        return Response(
            storage_service.stream_file(file),
            mimetype="video/mp4",
            headers={
                "Content-Disposition": f'attachment; filename="{file.name}"'
            }
        )

    return bp
