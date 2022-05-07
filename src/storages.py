from typing import Any, Optional

from shared.domain import BaseError


class StorageError(BaseError):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Storage error"
        super().__init__(message, *args, **kwargs)


class Storage:
    """
    Base Storage class. Use only for inheritance.
    NOTE: the subclass should have __slots__ defined
    NOTE: account_id used for future hashing in unique objects

    Usage example:
        In [1]: class AnalyticsStorage(Storage):
           ...:     __slots__ = "field_1", "field_2"
           ...:     def __init__(self, account_id: int, *_, **__):
           ...:         self.field_1: Optional[str] = None
           ...:         self.field_2: Optional[str] = None
    """

    _instances: dict[int, "Storage"] = {}

    def __new__(cls, account_id: int, *args, **kwargs) -> "Storage":
        if not hasattr(cls, "__slots__"):
            raise StorageError(f"You didn't define __slots__ for {cls.__name__}")

        key = cls.__get_unique_by_class_name(account_id)

        if key not in cls._instances:
            new_instance = super().__new__(cls)
            cls._instances[key] = new_instance
            return new_instance
        else:
            return cls._instances[key]

    def __init__(self, account_id: int) -> None:
        if getattr(self, "__initialized", False):
            return

        self.account_id: int = account_id
        setattr(self, "__initialized", True)

    @classmethod
    def __get_unique_by_class_name(cls, value: Any):
        return hash(str(value) + cls.__name__)
