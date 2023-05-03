from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: int
    firstname: str
    surname: str
    email: str
    role: str

    @classmethod
    def from_row(cls, row):
        return User(
            id=row[0],
            firstname=row[1],
            surname=row[2],
            email=row[3],
            role=row[4]
        )

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "firstname": self.firstname,
            "surname": self.surname,
            "email": self.email,
            "role": self.role
        }
