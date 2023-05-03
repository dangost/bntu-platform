from src.common.crypto import sha256
from src.models.user import User
from src.repositories.db_repo import DatabaseClient
from src.exceptions import IncorrectCurrentPassword


class UserService:
    def __init__(self, db_client: DatabaseClient):
        self.__db_client = db_client

    def change_password(self, user: User, current_pass: str, new_pass: str) -> None:
        current_hash = sha256(current_pass)
        new_hash = sha256(new_pass)

        email = self.__db_client.execute(
            f"select email from users where id={user.id} and password_hash='{current_hash}'",
            return_function=lambda r: r[0][0] if len(r) > 0 and len(r[0]) > 0 else None,
        )
        if email != user.email:
            raise IncorrectCurrentPassword()

        self.__db_client.execute(
            f"update users set password_hash='{new_hash}' where id={user.id}",
            commit=True,
        )

    def change_avatar(self, user: User, path: str) -> None:
        self.__db_client.execute(
            f"update users set avatar='{path}' where id={user.id}",
            commit=True
        )
