from flask import Flask

from src import Config
from src.repositories.db_repo import DatabaseClient
from src.services.auth_service import AuthService
from src.services.user_service import UserService


def init_services(app: Flask, config: Config) -> None:
    logger = config.logger
    logger.info("Services loaded")
    db_client = DatabaseClient(
        user=config.database_config.user,
        password=config.database_config.password,
        host=config.database_config.host,
        port=config.database_config.port,
        db=config.database_config.database,
    )
    app.config.auth_service = AuthService(db_client, config.server_config.jwt_secret)
    app.config.user_service = UserService(db_client)
