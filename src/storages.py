from typing import Any, Callable, Optional

from loguru import logger

from shared.domain import BaseError
from shared.messages import MESSAGE_DEPRICATED


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
           ...:         if getattr(self, "__initialized", False):
           ...:             return
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
        self.trash_messages: set[int] = set()
        setattr(self, "__initialized", True)

    @classmethod
    def __get_unique_by_class_name(cls, value: Any):
        return hash(str(value) + cls.__name__)

    def check_fields(self, *args):
        for arg in args:
            if getattr(self, arg, None) is None:
                logger.debug(f"{arg} -> Not set when check fields")
                raise BaseError(MESSAGE_DEPRICATED)

    def clean(self) -> None:
        data = self.__dict__
        for field in {key: data for key in data.keys() ^ "trash_messages"}:
            setattr(self, field, None)


class State:
    _instances: dict[int, Any] = {}

    def __new__(cls, account_id: int) -> "State":
        if account_id not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[account_id] = instance
            return instance
        return cls._instances[account_id]

    def __init__(self, account_id: int) -> None:
        if getattr(self, "__initialized", False):
            return

        self.account_id = account_id
        self.storage = None
        self.key = None
        self.validator: Optional[Callable] = None
        self.callback: Optional[Callable] = None

        setattr(self, "__initialized", True)

    def set(self, *_, storage: Storage, key: str, validator: Optional[Callable] = None, callback: Callable) -> None:
        self.validator = validator
        self.callback = callback
        self.storage = storage
        self.key = key

    def clean(self) -> None:
        self.validator = None
        self.callback = None
        self.storage = None
        self.key = None
