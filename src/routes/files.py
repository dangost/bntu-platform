from flask import Blueprint, jsonify, request, current_app as app

from src.repositories.minio_client import Folders
from src.services import AuthService, FilesService

files_api = Blueprint("files-api", __name__, url_prefix="/api/files")


@files_api.route("/upload", methods=['POST'])
def upload_file():
    files_service: FilesService = app.config.files_service
    auth_service: AuthService = app.config.auth_service
    token = request.headers.get("Authorization", None)
    host = request.host
    user = auth_service.auth(token, host)

    filename = request.json.get('filename')
    payload = request.json.get('base64')

    files_service.upload_file(user, filename, payload, Folders.FILES)

    return jsonify(
        {"status": 200, "message": "OK"}
    ), 200
