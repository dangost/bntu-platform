from flask import Blueprint, current_app as app, jsonify, request

from src.common.flask_auth import get_current_user

canteens_api = Blueprint("canteens_api", __name__, url_prefix="/api/canteens")


@canteens_api.route("/", methods=["GET"])
def get_canteens():
    # no auth
    canteens_service = app.config.canteens_service

    canteens = canteens_service.get_canteens()

    return [canteen.json for canteen in canteens]


@canteens_api.route("/update", methods=["POST"])
def update_menu():
    user = get_current_user()
    image = request.json().get("image")  # /api/images/1
    canteens_service = app.config.canteens_service

    canteens_service.update_menu(user, image)

    return jsonify(
        {
            "status": 200,
            "message": "OK"
        }
    )
