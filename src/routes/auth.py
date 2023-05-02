from flask import Blueprint, request, current_app as app

from src.models.authorization import LoginModel

auth = Blueprint("auth-api", __name__, url_prefix="/api/auth")


@auth.route("/login", methods=['POST'])
def login():
    body = request.json
    ip = request.host
    login_model = LoginModel.from_json(body, ip)


@auth.route("/signup", methods=['POST'])
def signup():
    pass
