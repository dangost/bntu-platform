from flask import Blueprint, jsonify, current_app as app, request

from src.models.posts import Post
from src.services import AuthService, UserService

posts_api = Blueprint("posts-api", __name__, url_prefix="/api/posts")


@posts_api.route("/", methods=["POST"])
def create_post():
    auth_service: AuthService = app.config.auth_service
    token = request.headers.get("Authorization", None)
    host = request.host
    user = auth_service.auth(token, host)

    user_service: UserService = app.config.user_service

    post = Post.from_json(request.json)
    user_service.create_post(user, post)

    return jsonify({"status": 200, "message": "OK"}), 200


@posts_api.route("/<int:user_id>", methods=["GET"])
def get_user_posts(user_id: int):
    auth_service: AuthService = app.config.auth_service
    token = request.headers.get("Authorization", None)
    host = request.host
    visitor = auth_service.auth(token, host)

    user_service: UserService = app.config.user_service

    posts = user_service.get_user_posts(visitor, user_id)

    return jsonify([post.to_json() for post in posts]), 200
