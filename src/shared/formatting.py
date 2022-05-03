from decimal import Decimal
from typing import Optional, Union


def get_number_in_frames(num: Optional[Union[int, float, Decimal]]) -> str:
    if not num:
        return ""
    return "{0:,}".format(num).replace(",", " ")
