from flask import Blueprint, request, current_app as app, jsonify

from src.services import AuthService

users_api = Blueprint("users_api", __name__, url_prefix="/api/users")


@users_api.route("/me", methods=['GET'])
def user_page():
    auth_service: AuthService = app.config.auth_service

    token = request.headers.get('Authorization', None)
    host = request.host

    user = auth_service.auth(token, host)
    return jsonify(user.to_json()), 200
