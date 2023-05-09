from flask import Blueprint, jsonify, request, current_app as app, send_file

from src.common.flask_auth import get_current_user
from src.common.json_loader import read_file_from_json
from src.exceptions import S3FileNotCreated
from src.repositories.minio_client import Folders
from src.services import FilesService

files_api = Blueprint("files-api", __name__, url_prefix="/api/files")


@files_api.route("/upload", methods=["POST"])
def upload_file():
    user = get_current_user()

    files_service: FilesService = app.config.files_service

    filename, payload = read_file_from_json(request.json)

    file_id, _ = files_service.upload_file(user, filename, payload, Folders.FILES)
    if not file_id:
        raise S3FileNotCreated()
    return jsonify({"status": 200, "message": "OK", "file_id": file_id}), 200


@files_api.route("/upload-image", methods=["POST"])
def upload_image():
    files_service: FilesService = app.config.files_service
    user = get_current_user()

    filename, payload = read_file_from_json(request.json)

    file_id, _ = files_service.upload_file(user, filename, payload, Folders.IMAGES)
    if not file_id:
        raise S3FileNotCreated()
    return jsonify({"status": 200, "message": "OK", "file_id": file_id}), 200


@files_api.route("/images/<int:image_id>", methods=["GET"])
def get_image(image_id: int):
    files_service: FilesService = app.config.files_service
    filename, data = files_service.get_image(image_id)

    return send_file(path_or_file=data, download_name=filename, mimetype="image/jpeg")
