import re

from db._postgres import Postgres
from db.constants import DB_ENGINES, DB_REGEX
from db.errors import DatabaseError
from db.models import ConnectionData
from db.protocols import Database


class DatabasesService:
    def __init__(
        self,
        host="postgres",
        port=5432,
        username="postgres",
        password="postgres",
        dbname="postgres",
    ) -> None:
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._dbname = dbname

        self._connection_url = ""
        self.connection_url_match: re.Match = self.__get_connection_url_match()

    def __get_connection_url_match(self) -> re.Match:
        try:
            result = re.search(DB_REGEX, self._connection_url)
            if result is None:
                raise DatabaseError(
                    f'Database connection string "{self._connection_url}" does not match with expected regex.'
                )
            return result
        except AttributeError:
            raise DatabaseError(
                f'Database connection string "{self._connection_url}" does not match with expected regex.'
            )
        except ValueError:
            raise DatabaseError(f'Port is invalid integer. Database connection string "{self._connection_url}".')

    def get_database(self) -> Database:
        engine = self.connection_url_match.group("db_engine")
        if engine == DB_ENGINES.POSTGRES.value:
            return Postgres(self.connection_data)

        raise DatabaseError("Can not find database engine.")

    @property
    def connection_data(self) -> ConnectionData:
        try:
            return ConnectionData(
                host=self._host,
                port=self._port,
                username=self._username,
                password=self._password,
                dbname=self._dbname,
            )
        except IndexError:
            raise DatabaseError("Something wrong with regex")
