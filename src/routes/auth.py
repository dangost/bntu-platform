from flask import Blueprint, request, current_app as app, make_response, jsonify

from src.models.authorization import LoginModel
from src.services.auth_service import AuthService

auth_api = Blueprint("auth-api", __name__, url_prefix="/api/auth")


@auth_api.route("/login", methods=["POST"])
def login():
    auth_service: AuthService = app.config.auth_service

    body = request.json
    ip = request.host
    login_model = LoginModel.from_json(body, ip)

    result = auth_service.login(login_model)

    response = make_response(jsonify({"status": 200, "message": "OK"}))
    response.status = 200
    response.headers = {"Authorization": result, "Content-Type": "application/json"}
    return response


@auth_api.route("/signup", methods=["POST"])
def signup():
    pass
