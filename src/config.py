from src.common.envs import string_env

# SERVER ENVS
SERVER_HOST = "SERVER_HOST"
SERVER_PORT = "SERVER_PORT"
SERVER_JWT_SECRET = "SERVER_JWT_SECRET"

# DATABASE ENVS
DB_HOST = "DB_HOST"
DB_PORT = "DB_PORT"
DB_USER = "DB_USER"
DB_PASSWORD = "DB_PASSWORD"
DB_DATABASE = "DB_DATABASE"


class ServerConfig:
    def __init__(self):
        self.host = string_env(SERVER_HOST)
        self.port = string_env(SERVER_PORT)
        self.jwt_secret = string_env(SERVER_JWT_SECRET)


class DatabaseConfig:
    def __init__(self):
        self.host = string_env(DB_HOST)
        self.port = string_env(DB_PORT)
        self.user = string_env(DB_USER)
        self.password = string_env(DB_PASSWORD)
        self.database = string_env(DB_DATABASE)


class Config:
    def __init__(self):
        self.server_config = ServerConfig()
        self.database_config = DatabaseConfig()
