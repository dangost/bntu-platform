from caspius import Logger

from src.common.envs import string_env, int_env
from src.exceptions import JWTSecretNotExists

# SERVER ENVS
SERVER_HOST = "SERVER_HOST"
SERVER_PORT = "SERVER_PORT"
SERVER_JWT_SECRET = "SERVER_JWT_SECRET"
SERVER_WORKERS = "SERVER_WORKERS"
SERVER_URL = "SERVER_URL"

# DATABASE ENVS
DB_HOST = "DB_HOST"
DB_PORT = "DB_PORT"
DB_USER = "DB_USER"
DB_PASSWORD = "DB_PASSWORD"
DB_DATABASE = "DB_DATABASE"

# LOGS
LOG_FILE = "LOG_FILE"

# MINIO
MINIO_HOST = "MINIO_HOST"
MINIO_PORT = "MINIO_PORT"
MINIO_ACCESS_KEY = "MINIO_ACCESS_KEY"
MINIO_SECRET_KEY = "MINIO_SECRET_KEY"


class ServerConfig:
    def __init__(self):
        self.host = string_env(SERVER_HOST, default="0.0.0.0")
        self.port = int_env(SERVER_PORT, default=28755)
        self.jwt_secret = string_env(SERVER_JWT_SECRET)
        self.server_url = string_env(SERVER_URL)
        self.workers = int_env(SERVER_WORKERS, default=1)
        if not self.jwt_secret:
            raise JWTSecretNotExists()


class DatabaseConfig:
    def __init__(self):
        self.host = string_env(DB_HOST)
        self.port = int_env(DB_PORT)
        self.user = string_env(DB_USER)
        self.password = string_env(DB_PASSWORD)
        self.database = string_env(DB_DATABASE)


class MinioConfig:
    def __init__(self):
        self.host = string_env(MINIO_HOST)
        self.port = string_env(MINIO_PORT)
        self.access_key = string_env(MINIO_ACCESS_KEY)
        self.secret_key = string_env(MINIO_SECRET_KEY)


class Config:
    def __init__(self):
        self.server_config = ServerConfig()
        self.database_config = DatabaseConfig()
        self.minio_config = MinioConfig()
        self.logger = Logger()
        self.logger.set_handler(self.log_handler)
        self.logger.info("Config loaded")

    @staticmethod
    def log_handler(log: str):
        with open("logs.txt", "a", encoding="utf-8") as fs:
            fs.write(f"\n{log}")
