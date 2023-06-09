from flask import Flask, jsonify, current_app

from src.config import Config
from src.exceptions import ServiceException
from src.repositories import init_repositories
from src.services import init_services
from src.routes import init_routes


def error_handler(exc: ServiceException):
    current_app.config.logger.warning(f"{exc.code} | {exc.message}")
    return jsonify({"status": exc.code, "message": exc.message}), exc.code


def exception_handler(exc: Exception):
    exc_str = str(exc)[1:-1]
    current_app.config.logger.warning(f"{exc_str}")
    return jsonify({"message": exc_str}), 500


def init_service(app: Flask, config_: Config) -> None:
    init_repositories(app, config_)
    init_services(app, config_)
    init_routes(app)

    app.config["JSON_SORT_KEYS"] = False
    # app.register_error_handler(Exception, exception_handler)
    app.register_error_handler(ServiceException, error_handler)
