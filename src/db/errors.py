from typing import Optional


class DatabaseError(Exception):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Database connection string does not match with expected regex."
        super().__init__(message, *args, **kwargs)
