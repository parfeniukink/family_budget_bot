from typing import Optional


class UserError(Exception):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Adding costs error"
        super().__init__(message, *args, **kwargs)
