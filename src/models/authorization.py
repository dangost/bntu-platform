from dataclasses import dataclass

from src.exceptions import LoginNotEnoughFields


@dataclass(frozen=True)
class LoginModel:
    login: str
    password: str
    ip_address: str

    @classmethod
    def from_json(cls, body: dict, ip_address: str):
        login = body.get("login", None)
        password = body.get("password", None)

        if None in (login, password, ip_address):
            raise LoginNotEnoughFields()

        return LoginModel(login=login, password=password, ip_address=ip_address)
