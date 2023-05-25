from flask import Blueprint, Response

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
