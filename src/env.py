import re
from os import getenv
from typing import Any, Optional


class EnvironmentError(Exception):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Can not parse the environment"
        super().__init__(message, *args, **kwargs)


class Env:
    @classmethod
    def __str_to_list(cls, value: str, sep=",") -> list[str]:
        return [i for i in value.split(sep) if i]

    @classmethod
    def list(cls, value: str, default: str = "") -> list:
        value = getenv(value, default)

        if not value and default:
            return cls.__str_to_list(default)
        if not value and not default:
            return cls.__str_to_list(value)

        try:
            return cls.__str_to_list(value)
        except Exception as e:
            raise EnvironmentError(str(e))

    @staticmethod
    def database_url(value: str, default=None) -> dict[str, Any]:
        DB_REGEX = (
            r"^(?P<engine>.*):\/\/((?P<username>[^:]*):(?P<password>[^@]*)@"
            r"(?P<host>[^:/]*)(:(?P<port>\d+))?\/)?(?P<name>.*)$"
        )
        result = re.search(DB_REGEX, getenv(value, default))

        if not result:
            raise EnvironmentError(f"Can not translate {value} into the database URL")

        return result.groupdict()

    @staticmethod
    def int(value: str, default: int = None) -> int:
        try:
            return int(str(getenv(value, default)))
        except ValueError as err:
            raise EnvironmentError(str(err))

    @staticmethod
    def str(value: str, default: str = None) -> str:
        return str(getenv(value, default))
