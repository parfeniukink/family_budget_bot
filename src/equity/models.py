from decimal import Decimal

from shared.collections import Model


class Equity(Model):
    id: int
    currency: str
    value: Decimal
