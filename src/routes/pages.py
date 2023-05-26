from http.cookies import SimpleCookie
from flask import Blueprint, Response, request, current_app as app

from src.common.flask_auth import get_current_user_from_cookie
from src.services import AuthService

pages = Blueprint("pages", __name__)


@pages.route("/", methods=["GET"])
def main_page():
    with open("views/index.html", "r", encoding="UTF-8") as fs:
        data: str = fs.read()
    response = Response(response=data, status=200, content_type="text/html")
    return response


@pages.route("/<filename>", methods=["GET"])
def html(filename: str):
    try:
        with open(f"views/{filename}", "r", encoding="UTF-8") as fs:
            data: str = fs.read()
        response = Response(response=data, status=200, content_type="text/html")
    except FileNotFoundError:
        print(f"{filename} not found")
        return Response(status=404)
    return response


@pages.route("/auth", methods=["GET"])
def auth():
    with open(f"views/authorization.html", "r", encoding="UTF-8") as fs:
        data: str = fs.read()
    return Response(response=data, status=200, content_type="text/html")


@pages.route("/users/<int:user_id>")
def user_pages(user_id: int):
    get_current_user_from_cookie()
    with open(f"views/teacher_view.html", 'r', encoding="UTF-8") as fs:
        data = fs.read()
    return Response(response=data, status=200, content_type="text/html")


@pages.route("/me", methods=["GET"])
def me():
    user = get_current_user_from_cookie()
    data = ""
    if user.role == 'Student':
        with open(f"views/student.html", "r", encoding="UTF-8") as fs:
            data = fs.read()
    elif user.role == "Teacher":
        with open(f"views/teacher.html", "r", encoding="UTF-8") as fs:
            data = fs.read()
    response = Response(response=data, status=200, content_type="text/html")
    return response


@pages.route('/css/<filename>')
def css(filename: str):
    with open(f"views/css/{filename}", 'r') as fs:
        data: str = fs.read()
    response = Response(response=data, status=200, content_type="text/css")
    return response


@pages.route('/js/<filename>')
def js(filename: str):
    with open(f"views/js/{filename}", 'r') as fs:
        data: str = fs.read()
    response = Response(response=data, status=200, content_type="application/js")
    return response


@pages.route('/img/<filename>')
def img(filename: str):
    with open(f"views/img/{filename}", 'rb') as fs:
        data: bytes = fs.read()
    response = Response(response=data, status=200, content_type="image/jpg")
    return response
