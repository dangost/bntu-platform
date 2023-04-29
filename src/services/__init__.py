from flask import Flask

from src import Config


def init_services(app: Flask, config: Config) -> None:
    logger = config.logger
    logger.info("Services loaded")
    pass
