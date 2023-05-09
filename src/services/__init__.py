from flask import Flask

from src import Config
from src.repositories.db_repo import DatabaseClient
from src.repositories.minio_client import MinioClient
from src.services.auth_service import AuthService
from src.services.divisions_service import DivisionsService
from src.services.files_service import FilesService
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

    minio_client = MinioClient(
        access_key=config.minio_config.access_key,
        secret_key=config.minio_config.secret_key,
        host=config.minio_config.host,
        port=config.minio_config.port,
    )

    app.config.auth_service = AuthService(db_client, config.server_config.jwt_secret)
    app.config.user_service = UserService(db_client, minio_client)
    app.config.files_service = FilesService(db_client, minio_client)
    app.config.divisions_service = DivisionsService(db_client)
