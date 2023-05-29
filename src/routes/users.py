from flask import Blueprint, request, current_app as app, jsonify

from src.common.flask_auth import get_current_user
from src.exceptions import UnauthorizedException
from src.repositories.minio_client import Folders
from src.services import FilesService
from src.services.user_service import UserService

users_api = Blueprint("users_api", __name__, url_prefix="/api/users")


@users_api.route("/me", methods=["GET"])
def user_page():
    user = get_current_user()
    return jsonify(user.to_json()), 200


@users_api.route("/me-student", methods=["GET"])
def student_page():
    user = get_current_user()
    user_service: UserService = app.config.user_service

    student = user_service.get_student(user.id)
    return jsonify(student.json), 200


@users_api.route("/me-teacher", methods=["GET"])
def teacher_page():
    user = get_current_user()
    if user.role != "Teacher":
        raise UnauthorizedException()
    user_service: UserService = app.config.user_service

    teacher = user_service.get_teacher(user.id)

    return jsonify(teacher.json), 200


@users_api.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id: int):
    get_current_user()
    user_service: UserService = app.config.user_service

    student = user_service.get_student(student_id)

    return jsonify(student.json), 200


@users_api.route("/teachers/<int:teacher_id>", methods=["GET"])
def get_teacher(teacher_id: int):
    get_current_user()
    user_service: UserService = app.config.user_service

    teacher = user_service.get_teacher(teacher_id)

    return jsonify(teacher.json), 200


@users_api.route("/dep-teachers/<int:dep_id>", methods=["GET"])
def get_department_teachers(dep_id: int):
    get_current_user()
    user_service: UserService = app.config.user_service

    teachers = user_service.department_teachers(dep_id)

    return jsonify([teacher.json for teacher in teachers])


@users_api.route("/change-password", methods=["POST"])
def reset_password():
    user_service: UserService = app.config.user_service
    user = get_current_user()

    current = request.json.get("current_password", None)
    new = request.json.get("new_password", None)
    user_service.change_password(user, current, new)

    return jsonify({"status": 200, "message": "Password was changed"}), 200


@users_api.route("/change-avatar", methods=["POST"])
def change_avatar():
    user = get_current_user()

    user_service: UserService = app.config.user_service
    files_service: FilesService = app.config.files_service
    filename = request.json.get("filename")
    payload = request.json.get("base64")
    file_id, _ = files_service.upload_file(
        user, filename, payload, folder=Folders.IMAGES
    )
    path = f"/api/files/images/{file_id}"
    user_service.change_avatar(user, path)

    return jsonify({"status": 200, "message": "OK"}), 200
