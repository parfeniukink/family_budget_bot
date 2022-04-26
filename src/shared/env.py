from typing import Optional


class EnvironmentError(Exception):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Can not parse the environment"
        super().__init__(message, *args, **kwargs)


class Env:
    @staticmethod
    def list(value: str = "") -> list:
        if not value:
            return []
        try:
            return [i for i in value.split(",") if i]
        except Exception as e:
            raise EnvironmentError(str(e))
