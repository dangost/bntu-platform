from flask import Flask

from src.routes.auth import auth_api
from src.routes.files import files_api
from src.routes.pages import pages
from src.routes.users import users_api


def init_routes(app: Flask) -> None:
    app.register_blueprint(pages)
    app.register_blueprint(auth_api)
    app.register_blueprint(users_api)
    app.register_blueprint(files_api)
