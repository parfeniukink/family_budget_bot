from db._postgres import Postgres
from db.domain import DB_ENGINES, ConnectionData, DatabaseError
from db.protocols import Database
from settings import DATABASE_URL

__all__ = ("database",)


class DatabasesService:
    """Main databases handler"""

    def __init__(
        self,
        *_,
        engine="postgresql",
        host="postgres",
        port=5432,
        username="postgres",
        password="postgres",
        name="postgres",
        **__,
    ) -> None:
        self._engine = engine
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._name = name

        self._connection_url = ""
        self.connection_url_match = None

        # NOTE: Run database init
        self.__init_database()

    def __init_database(self):
        database: Database = self.get_database()
        database.init()

    def get_database(self) -> Database:
        if self._engine == DB_ENGINES.POSTGRES.value:
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
                dbname=self._name,
            )
        except IndexError:
            raise DatabaseError("Something wrong with regex")


__database_service = DatabasesService(**DATABASE_URL)

database = __database_service.get_database()
