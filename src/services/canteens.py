from src.models.canteens import Canteen
from src.repositories.db_repo import DatabaseClient


class CanteensService:
    def __init__(self, db_client: DatabaseClient):
        self.__db_client = db_client

    def get_canteens(self) -> list[Canteen]:
        canteens = self.__db_client.execute(
            "select id, name, description, address, avatar, current_menu from canteens;"
        )

        return [Canteen.from_row(row) for row in canteens]

    def update_menu(self, admin: str, image: str) -> None:
        self.__db_client.execute(
            f"update canteens set current_menu='{image}' where admin = {admin};"
        )

        return None

