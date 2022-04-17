from typing import Optional

from shared.errors import UserError


class AnalyticsError(UserError):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Analytics Error"
        super().__init__(message, *args, **kwargs)
