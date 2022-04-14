from pydantic import validator

from shared.collections import Model


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
