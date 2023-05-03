import jwt

from src.common.crypto import sha256
from src.db.database_client import DatabaseClient
from src.exceptions import UnauthorizedException
from src.models.authorization import LoginModel
from src.models.user import User


JWT_TOKEN = str


class AuthService:
    def __init__(self, db_client: DatabaseClient, jwt_secret: str):
        self.jwt_secret = jwt_secret
        self.db_client = db_client
        self.algorithm = "HS256"

    def login(self, login_model: LoginModel) -> JWT_TOKEN:
        hash_password = sha256(login_model.password)
        user_id = self.db_client.execute(
            f"select id from users "
            f"where email='{login_model.login}' and password_hash='{hash_password}'",
            return_function=lambda result: result[0][0]
            if len(result) > 0 and len(result[0]) > 0
            else None,
        )
        if not user_id:
            raise UnauthorizedException()
        token = jwt.encode(
            payload={"login": login_model.login, "ip_address": login_model.ip_address},
            key=self.jwt_secret,
            algorithm=self.algorithm,
        )
        return token

    def signup(self) -> (User, JWT_TOKEN):
        pass

    def auth(self, token: str, ip_address: str) -> User:
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.algorithm])
        except jwt.exceptions.PyJWTError:
            raise UnauthorizedException()
        login = payload["login"]
        if ip_address != payload["ip_address"]:
            raise UnauthorizedException()
        result = self.db_client.execute(
            f"select u.id, firstname, surname, email, r.name, avatar from users u "
            f"inner join roles r on r.id = u.role_id "
            f"where email='{login}' limit 1"
        )

        if not result or not result[0]:
            raise UnauthorizedException()

        return User.from_row(result[0])
