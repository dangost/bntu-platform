from abc import ABC

import psycopg2


class BaseService(ABC):
    def __init__(self, connection: psycopg2.connect):
        self._connection = connection
        self._cursor = self._connection.cursor()

    def new_cursor(self):
        return self._connection.cursor()

    def commit(self):
        self._connection.commit()

    def close(self):