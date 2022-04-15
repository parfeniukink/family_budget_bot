from datetime import date
from decimal import Decimal

from shared.collections import Model


class Income(Model):
    id: int
    name: str
    value: Decimal
    currency: str
    date: date
    user_id: int
