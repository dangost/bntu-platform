from http.cookies import SimpleCookie
from typing import Optional

from flask import request, current_app as app
from src.models.user import User
from src.services import AuthService


def get_current_user() -> User:
    auth_service: AuthService = app.config.auth_service
    token = request.headers.get("Authorization", None)
    host = request.host
    user = auth_service.auth(token, host)
    return user


def get_current_user_from_cookie() -> Optional[User]:
    raw_data = request.headers.get('COOKIE', None)
    if raw_data is None:
        return None
    auth_service: AuthService = app.config.auth_service
    simple_cookie = SimpleCookie()
    simple_cookie.load(raw_data)
    token = ""
    for n, v in simple_cookie.items():
        if n == 'auth':
            token = v.coded_value
            break
    host = request.host
    user = auth_service.auth(token, host)
    return user