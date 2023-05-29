from flask import Blueprint, current_app as app, jsonify, request

from src.common.flask_auth import get_current_user
from src.models.retakes import RetakeBody
from src.services import RetakesService

retakes_api = Blueprint("retakes_api", __name__, url_prefix="/api/retakes")


@retakes_api.route("/", methods=['GET'])
def get_retakes():
    user = get_current_user()
    retakes_service: RetakesService = app.config.retakes_service
    retakes = []
    if user.role == "Student":
        retakes = retakes_service.get_student_retakes(user.id)
    elif user.role == "Teacher":
        retakes = retakes_service.get_teacher_retakes(user.id)
    return jsonify([retake.json for retake in retakes])


@retakes_api.route("/", methods=['POST'])
def create_retake():
    user = get_current_user()
    retakes_service: RetakesService = app.config.retakes_service
    retake = RetakeBody.from_json(request.json)
    retakes_service.create_retake(user.id, retake)
    return jsonify(
        {
            "status": 200,
            "message": "OK"
        }
    )
