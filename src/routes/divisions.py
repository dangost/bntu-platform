from flask import request, jsonify, current_app as app, Blueprint

from src.common.flask_auth import get_current_user
from src.exceptions import DivisionNotFound

divisions_api = Blueprint("divisions_api", __name__, url_prefix="/api/divisions")


@divisions_api.route("/faculties", methods=["GET"])
def get_faculties():
    # no auth
    divisions_service = app.config.divisions_service

    faculties = divisions_service.faculties()

    return jsonify(faculties.json)


@divisions_api.route("/departments/<int:faculty_id>", methods=["GET"])
def get_departments(faculty_id: int):
    # no auth
    if not faculty_id:
        raise DivisionNotFound("Faculty")

    divisions_service = app.config.divisions_service
    departments = divisions_service.departments(int(faculty_id))

    return jsonify(departments.json)


@divisions_api.route("/groups", methods=["GET"])
def get_groups():
    get_current_user()  # auth

    dep_id = request.args.get("department", None)
    if not dep_id:
        raise DivisionNotFound("Department")

    divisions_service = app.config.divisions_service

    groups = divisions_service.groups(int(dep_id))

    return jsonify(groups.json)


@divisions_api.route("/groups/<int:group_id>", methods=["GET"])
def get_full_group(group_id: int):
    get_current_user()
    divisions_service = app.config.divisions_service
    student = divisions_service.get_group(group_id)

    return jsonify(student.json), 200
