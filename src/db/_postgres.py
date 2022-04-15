from contextlib import contextmanager, suppress
from typing import Any, Optional

import psycopg2
from loguru import logger

from db.constants import SCRIPTS_FOLDER
from db.models import ConnectionData


# Follows Database protocol
class Postgres:
    def __init__(self, connection_data: ConnectionData) -> None:
        self._connection_data = connection_data

    def _get_connection(self) -> Any:
        return psycopg2.connect(
            host=self._connection_data.host,
            dbname=self._connection_data.dbname,
            user=self._connection_data.username,
            password=self._connection_data.password,
        )

    @contextmanager
    def cursor(self):
        """Database cursoor context manager"""
        connection = self._get_connection()
        try:
            yield connection.cursor()
        finally:
            if connection:
                connection.commit()
                connection.close()

    def __create_new_tables(self) -> None:
        filename = SCRIPTS_FOLDER / "init_tables.sql"
        with open(filename) as f:
            query = f.read()
        with self.cursor() as cursor:
            cursor.execute(query)
        logger.success("Tables created")

    def init(self) -> None:
        try:
            with self.cursor() as cursor:
                cursor.execute("SELECT * FROM users")
            logger.info("Tables exist")
        except psycopg2.errors.UndefinedTable:  # type: ignore
            logger.info("Creating new tables")
            self.__create_new_tables()

    def insert(self, table: str, data: dict[str, Any]) -> None:
        columns = ", ".join(str(k) for k in data.keys())
        values = ", ".join(
            [v if v.isdigit() else "".join(["'", v, "'"]) for value in data.values() if (v := str(value))]
        )
        q = f"INSERT INTO {table} ({columns}) VALUES ({values})"

        with self.cursor() as cursor:
            cursor.execute(q)

    def __fetch_data_as_dict(self, data: list[tuple], description: tuple) -> list[dict]:
        columns = [d[0] for d in description]
        results = []

        for item in data:
            dict_row = {}
            for index, column in enumerate(columns):
                dict_row[column] = item[index]

            results.append(dict_row)

        return results

    def fetch(self, table: str, column: str, value: Any) -> Optional[dict]:
        q = f"SELECT * FROM {table} WHERE {column} = {value}"

        with self.cursor() as cursor:
            cursor.execute(q)
            data: list[tuple] = cursor.fetchall()
            with suppress(IndexError):
                results = self.__fetch_data_as_dict(data, cursor.description)
                return results[0]
            return None
