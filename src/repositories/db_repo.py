from typing import Optional

import psycopg2


class DatabaseClient:
    def __init__(
        self,
        user: str,
        password: str,
        db: str = "postgres",
        host: str = "127.0.0.1",
        port: int = 5432,
    ):
        self.__credentials = {
            "user": user,
            "host": host,
            "port": port,
            "password": password,
            "database": db,
        }
        self._connection = psycopg2.connect(**self.__credentials)
        self._cursor = self._connection.cursor()

    def reconnect(self):
        self.close()
        self._connection = psycopg2.connect(**self.__credentials)
        self.new_cursor()

    def new_cursor(self):
        self.close()
        self._cursor = self._connection.cursor()
        return self._cursor

    def commit(self):
        self._connection.commit()

    def fetchall(self) -> list[tuple]:
        return self._cursor.fetchall()

    def execute(
        self, query: str, commit: bool = False, return_function=None
    ) -> Optional[list]:
        cursor = self._connection.cursor()
        cursor.execute(query)
        if commit:
            self.commit()
        if query.lower().startswith("select"):
            result = cursor.fetchall()
            if not return_function:
                return result if result else None
            handled = return_function(result)
            return handled if handled else None
        return None

    def execute_queryset(self, queryset: list, commit: bool = False) -> None:
        with self._connection.cursor() as cursor:
            for query in queryset:
                cursor.execute(query)
        if commit:
            self.commit()

    def close(self):
        self._cursor.close()
        self._connection.close()
