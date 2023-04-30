from flask import Flask

from src.routes.pages import pages


def init_routes(app: Flask) -> None:
    app.register_blueprint(pages)
