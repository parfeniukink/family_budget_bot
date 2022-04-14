from datetime import date
from decimal import Decimal

from shared.collections import Model


class Category(Model):
    id: int
    name: str


class Cost(Model):
    id: int
    name: str
    value: Decimal
    currency: str
    date: date
    user_id: int
    category_id: int
