from contextlib import contextmanager, suppress
from typing import Any, Optional

import psycopg2
from loguru import logger

from db.domain import ConnectionData
from settings import ROOT_FOLDER

SCRIPTS_DIR = ROOT_FOLDER / "scripts"


class Postgres:
    """This class follows src/db/protocols.py:Protocol"""

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
        filename = SCRIPTS_DIR / "db/init_tables.sql"
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

    def __fetch_data_as_dict(self, data: list[tuple], description: tuple) -> list[dict]:
        results = [{k[0]: v for k, v in zip(description, d)} for d in data]
        return results

    def execute(self, q: str) -> None:
        with self.cursor() as cursor:
            cursor.execute(rf"{q}")

    def raw_execute(self, q: str) -> list[dict]:
        with self.cursor() as cursor:
            cursor.execute(rf"{q}")
            data = cursor.fetchall()
        return [{k[0]: v for k, v in zip(cursor.description, d)} for d in data]

    def fetchall(self, table: str, columns: Optional[str] = None) -> list[dict]:
        q = f"SELECT {columns or '*'} FROM {table}"

        with self.cursor() as cursor:
            cursor.execute(q)
            data: list[tuple] = cursor.fetchall()
            with suppress(IndexError):
                return self.__fetch_data_as_dict(data, cursor.description)
            return []

    def fetch(self, table: str, column: str, value: Any) -> list[dict]:
        value = value if str(value).isdigit() else "".join(("'", value, "'"))
        q = f"SELECT * FROM {table} WHERE {column} = {value}"

        with self.cursor() as cursor:
            cursor.execute(q)
            data: list[tuple] = cursor.fetchall()
            with suppress(IndexError):
                results = self.__fetch_data_as_dict(data, cursor.description)
                return results
            return []

    def fetchone(self, table: str, column: str, value: Any) -> Optional[dict]:
        try:
            return self.fetch(table=table, column=column, value=value)[0]
        except IndexError:
            return None

    def insert(self, table: str, data: dict[str, Any]) -> dict:
        columns = ", ".join(str(k) for k in data.keys())
        values = ", ".join(
            [
                v
                if v.isdigit()
                else "".join(
                    ["'", v, "'"],
                )
                for value in data.values()
                if (v := str(value)) is not None
            ]
        )
        q = f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING *"

        with self.cursor() as cursor:
            cursor.execute(q)
            execution_result = cursor.fetchone()

        result = {k[0]: v for k, v in zip(cursor.description, execution_result)}

        return result

    def update(self, table: str, data: tuple[str, Any], condition: tuple[str, Any]) -> dict:
        f_data = "=".join([data[0], fd if (fd := str(data[1])).isdigit() else "".join(["'", fd, "'"])])
        f_condition = "=".join([condition[0], fd if (fd := str(condition[1])).isdigit() else "".join(["'", fd, "'"])])

        q = f"UPDATE {table} SET {f_data} WHERE {f_condition} RETURNING *"

        with self.cursor() as cursor:
            cursor.execute(q)
            execution_result = cursor.fetchone()

        result = {k[0]: v for k, v in zip(cursor.description, execution_result)}

        return result

    def delete(self, table: str, column: str, value: str) -> dict:
        value = value if str(value).isdigit() else f"'{value}'"
        q = f"DELETE from {table} WHERE {column}={value} RETURNING *"

        with self.cursor() as cursor:
            cursor.execute(q)
            execution_result = cursor.fetchone()

        result = {k[0]: v for k, v in zip(cursor.description, execution_result)}

        return result
