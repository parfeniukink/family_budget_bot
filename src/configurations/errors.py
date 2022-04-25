from typing import Optional

from shared.errors import UserError


class ConfigurationError(UserError):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Configuration error"
        super().__init__(message, *args, **kwargs)
