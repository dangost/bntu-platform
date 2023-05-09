from flask import Blueprint, jsonify, current_app as app, request

from src.common.flask_auth import get_current_user
from src.models.posts import Post
from src.services import UserService

posts_api = Blueprint("posts-api", __name__, url_prefix="/api/posts")


@posts_api.route("/", methods=["POST"])
def create_post():
    user = get_current_user()

    user_service: UserService = app.config.user_service

    post = Post.from_json(request.json)
    user_service.create_post(user, post)

    return jsonify({"status": 200, "message": "OK"}), 200


@posts_api.route("/<int:user_id>", methods=["GET"])
def get_user_posts(user_id: int):
    visitor = get_current_user()

    user_service: UserService = app.config.user_service

    posts = user_service.get_user_posts(visitor, user_id)

    return jsonify([post.to_json() for post in posts]), 200
