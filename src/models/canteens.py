from dataclasses import dataclass


@dataclass(frozen=True)
class Canteen:
    id: int
    name: str
    description: str
    address: str
    avatar: str
    current_menu: str

    @classmethod
    def from_row(cls, row):
        return Canteen(
            id=row[0],
            name=row[1],
            description=row[2],
            address=row[3],
            avatar=row[4],
            current_menu=row[5]
        )

    @property
    def json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "avatar": self.avatar,
            "current_menu": self.current_menu
        }