from decimal import Decimal
from typing import Union


def get_number_in_frames(num: Union[int, float, Decimal]) -> str:
    return "{0:,}".format(num).replace(",", " ")
