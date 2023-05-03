from flask import Blueprint, Response

pages = Blueprint("pages", __name__)


@pages.route("/", methods=["GET"])
def main_page():
    with open("views/html/index.html", "r", encoding="UTF-8") as fs:
        data: str = fs.read()
    response = Response(response=data, status=200, content_type="text/html")
    return response
