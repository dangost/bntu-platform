import psycopg2

from src.models.user import User

JWT_TOKEN = str


class AuthService:
    def __init__(self, connection: psycopg2.connect, jwt_secret: str):
        self._connection = connection
        self.jwt_secret = jwt_secret

    def login(self) -> JWT_TOKEN:
        pass

    def signup(self) -> (User, JWT_TOKEN):
        pass

    def auth(self) -> User:
        pass
