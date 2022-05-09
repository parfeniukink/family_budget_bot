from typing import Optional

from shared.domain import BaseError, Model


class CategoriesError(BaseError):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "No such category"
        super().__init__(message, *args, **kwargs)


class Category(Model):
    id: int
    name: str
