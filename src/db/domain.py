from pydantic import validator

from shared.domain import Enum, Model

__all__ = ("DatabaseError",)


class DatabaseError(Exception):
    def __init__(self, message: str | None = None, *args, **kwargs) -> None:
        message = message or "Database connection string does not match with expected regex."
        super().__init__(message, *args, **kwargs)


class DB_ENGINES(Enum):
    POSTGRES = "postgresql"


class ConnectionData(Model):
    host: str = None  # type:ignore
    port: int = None  # type:ignore
    username: str = None  # type:ignore
    password: str = None  # type:ignore
    dbname: str = None  # type:ignore

    @validator("host")
    def set_default_host(cls, value: str) -> str:
        return value or "localhost"

    @validator("username", "password", "dbname")
    def set_default_username_password_name(cls, value: str) -> str:
        return value or "postgres"

    @validator("port")
    def set_default_port(cls, value: int) -> int:
        return value or 5432
