from typing import Optional

from shared.errors import UserError


class IncomesError(UserError):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Adding incomes error"
        super().__init__(message, *args, **kwargs)
