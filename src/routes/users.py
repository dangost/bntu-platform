from flask import Blueprint, request, current_app as app, jsonify

from src.repositories.minio_client import Folders
from src.services import AuthService, FilesService
from src.services.user_service import UserService

users_api = Blueprint("users_api", __name__, url_prefix="/api/users")


@users_api.route("/me", methods=["GET"])
def user_page():
    auth_service: AuthService = app.config.auth_service
    token = request.headers.get("Authorization", None)
    host = request.host
    user = auth_service.auth(token, host)

    return jsonify(user.to_json()), 200


@users_api.route("/change-password", methods=["POST"])
def reset_password():
    auth_service: AuthService = app.config.auth_service
    user_service: UserService = app.config.user_service
    token = request.headers.get("Authorization", None)
    host = request.host
    user = auth_service.auth(token, host)

    current = request.json.get("current_password", None)
    new = request.json.get("new_password", None)
    user_service.change_password(user, current, new)

    return jsonify({"status": 200, "message": "Password was changed"}), 200


@users_api.route("/change-avatar", methods=['POST'])
def change_avatar():
    auth_service: AuthService = app.config.auth_service
    token = request.headers.get("Authorization", None)
    host = request.host
    user = auth_service.auth(token, host)

    user_service: UserService = app.config.user_service
    files_service: FilesService = app.config.files_service
    filename = request.json.get("filename")
    payload = request.json.get("base64")
    file_id, _ = files_service.upload_file(user, filename, payload, folder=Folders.IMAGES)
    path = f"/api/files/images/{file_id}"
    user_service.change_avatar(user, path)

    return jsonify({"status": 200, "message": "OK"}), 200
