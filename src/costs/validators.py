from decimal import Decimal, DecimalException

from costs.domain import CostsError


def cost_value_validator(value: str) -> None:
    """Check if string value is valid to be a cost"""

    try:
        converted_value = Decimal(value)
    except DecimalException:
        raise CostsError("Value should be a valid number")

    if converted_value < 0:
        raise CostsError("Value should be greater than 0")
