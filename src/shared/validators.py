from decimal import Decimal, DecimalException

from shared.domain import BaseError


def money_value_validator(value: str) -> None:
    """Check if string value is valid to be a cost"""

    try:
        converted_value = Decimal(value)
    except DecimalException:
        raise BaseError("Value should be a valid number")

    if converted_value < 0:
        raise BaseError("Value should be greater than 0")
