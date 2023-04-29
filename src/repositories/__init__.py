from flask import Flask

from src import Config


def init_repositories(app: Flask, config: Config) -> None:
    logger = config.logger
    logger.info("Repositories loaded")
