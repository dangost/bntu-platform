from flask import Blueprint, Response, redirect

from src.common.flask_auth import get_current_user_from_cookie
from src.exceptions import UnauthorizedException

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
    with open("views/authorization.html", "r", encoding="UTF-8") as fs:
        data: str = fs.read()
    return Response(response=data, status=200, content_type="text/html")


@pages.route("/users/<int:user_id>")
def user_pages(user_id: int):
    get_current_user_from_cookie()
    with open("views/teacher_view.html", "r", encoding="UTF-8") as fs:
        data = fs.read()
    return Response(response=data, status=200, content_type="text/html")


@pages.route("/me", methods=["GET"])
def me():
    try:
        user = get_current_user_from_cookie()
    except UnauthorizedException:
        user = None
    if user is None:
        return redirect("/auth", code=401, Response=None)
    data = ""
    if user.role == "Student":
        with open("views/student.html", "r", encoding="UTF-8") as fs:
            data = fs.read()
    elif user.role == "Teacher":
        with open("views/teacher.html", "r", encoding="UTF-8") as fs:
            data = fs.read()
    response = Response(response=data, status=200, content_type="text/html")
    return response


@pages.route("/faculties", methods=["GET"])
def get_faculties():
    with open("views/faculties.html", "r", encoding="UTF-8") as fs:
        data = fs.read()
    return Response(response=data, status=200, content_type="text/html")


@pages.route("/canteens", methods=["GET"])
def canteens_page():
    with open("views/canteens.html", "r", encoding="UTF-8") as fs:
        data = fs.read()
    return Response(response=data, status=200, content_type="text/html")


@pages.route("/canteen-worker", methods=["GET"])
def canteen_worker_page():
    with open("views/canteen_worker.html", "r", encoding="UTF-8") as fs:
        data = fs.read()
    return Response(response=data, status=200, content_type="text/html")


@pages.route("/deans-office", methods=["GET"])
def deans_office():
    with open("views/deans_office.html", "r", encoding="UTF-8") as fs:
        data = fs.read()
    return Response(response=data, status=200, content_type="text/html")


@pages.route("/departments/<int:faculty_id>", methods=["GET"])
def get_deps(faculty_id: int):
    with open("views/departments.html", "r", encoding="UTF-8") as fs:
        data = fs.read()
    return Response(response=data, status=200, content_type="text/html")


@pages.route("/groups/<int:department_id>", methods=["GET"])
def get_dep_groups(department_id: int):
    get_current_user_from_cookie()
    with open("views/groups.html", "r", encoding="UTF-8") as fs:
        data = fs.read()
    return Response(response=data, status=200, content_type="text/html")


@pages.route("/group/<int:group_id>", methods=["GET"])
def get_group(group_id: int):
    get_current_user_from_cookie()
    with open("views/group.html", "r", encoding="UTF-8") as fs:
        data = fs.read()
    return Response(response=data, status=200, content_type="text/html")


@pages.route("/css/<filename>")
def css(filename: str):
    with open(f"views/css/{filename}", "r", encoding="UTF-8") as fs:
        data: str = fs.read()
    response = Response(response=data, status=200, content_type="text/css")
    return response


@pages.route("/js/<filename>")
def js(filename: str):
    with open(f"views/js/{filename}", "r", encoding="UTF-8") as fs:
        data: str = fs.read()
    response = Response(response=data, status=200, content_type="application/js")
    return response


@pages.route("/img/<filename>")
def img(filename: str):
    with open(f"views/img/{filename}", "rb") as fs:
        data: bytes = fs.read()
    response = Response(response=data, status=200, content_type="image/jpg")
    return response
