from flask import Blueprint, jsonify, request, current_app as app, send_file

from src.exceptions import S3FileNotCreated
from src.repositories.minio_client import Folders
from src.services import AuthService, FilesService

files_api = Blueprint("files-api", __name__, url_prefix="/api/files")


@files_api.route("/upload", methods=["POST"])
def upload_file():
    files_service: FilesService = app.config.files_service
    auth_service: AuthService = app.config.auth_service
    token = request.headers.get("Authorization", None)
    host = request.host
    user = auth_service.auth(token, host)

    filename = request.json.get("filename")
    payload = request.json.get("base64")

    file_id, _ = files_service.upload_file(user, filename, payload, Folders.FILES)
    if not file_id:
        raise S3FileNotCreated()
    return jsonify({"status": 200, "message": "OK", "file_id": file_id}), 200


@files_api.route("/images/<int:image_id>", methods=["GET"])
def get_image(image_id: int):
    files_service: FilesService = app.config.files_service
    filename, data = files_service.get_image(image_id)

    return send_file(path_or_file=data, download_name=filename, mimetype="image/jpeg")
