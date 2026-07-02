from flask import Blueprint, jsonify, request, send_file
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
            return {"status": "error", "message": f"File {data["filename"]} not found"}, 404

        return send_file(
            file,
            mimetype="video/mp4",
            as_attachment=True,
            download_name=file.name,
        )

    @bp.route("/storage/delete", methods=["POST"])
    def delete_file():
        data = request.get_json(silent=True)

        if not data or "filenames" not in data:
            return {"status": "error", "message": 'Missing "filenames" on request'}, 400

        filenames = data["filenames"]

        if not isinstance(filenames, list):
            return {"status": "error", "message": "Filenames must be a list"}, 400

        success, filename = storage_service.delete_file(filenames)
        if not success:
            return {"status": "error", "message": f"File {filename} not found"}, 404

        return {"status": "ok", "message": "Files deleted succesfully"}, 200

    return bp
