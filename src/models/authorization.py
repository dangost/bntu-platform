from dataclasses import dataclass

from src.exceptions import LoginNotEnoughFields


@dataclass(frozen=True)
class LoginModel:
    username: str
    password: str
    ip_address: str

    @classmethod
    def from_json(cls, body: dict, ip_address: str):
        username = body.get('username', None)
        password = body.get('password', None)

        if None in (username, password, ip_address):
            raise LoginNotEnoughFields()

        return LoginModel(
            username=username,
            password=password,
            ip_address=ip_address
        )
