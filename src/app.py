from flask import Flask

from src import init_service
from src.config import Config


def create_app(config: Config) -> Flask:
    app = Flask("Platform")
    app.config.logger = config.logger
    init_service(app, config)
    config.logger.info("App created")
    return app
