from flask import request, current_app as app
from src.models.user import User
from src.services import AuthService


def get_current_user() -> User:
    auth_service: AuthService = app.config.auth_service
    token = request.headers.get("Authorization", None)
    host = request.host
    user = auth_service.auth(token, host)
    return user
