from decimal import Decimal
from typing import Union


def get_number_in_frames(num: Union[int, float, Decimal] | None = None) -> str:
    return "{0:,}".format(num).replace(",", " ") if num is not None else ""
