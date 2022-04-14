from enum import Enum as _Enum
from enum import IntEnum as _IntEnum
from enum import unique
from typing import Iterable

from pydantic import BaseModel, Extra


@unique
class Enum(_Enum):
    @classmethod
    def values(cls: Iterable) -> list:
        return [i.value for i in cls]


@unique
class IntEnum(_IntEnum):
    @classmethod
    def values(cls: Iterable) -> list:
        return [i.value for i in cls]

    @classmethod
    def names(cls: Iterable) -> list:
        return [i.name for i in cls]


class Model(BaseModel):
    class Config:
        extra = Extra.ignore
        orm_mode = True
        use_enum_values = True
        allow_population_by_field_name = True
        validate_assignment = True
