from decimal import Decimal

from shared.domain import Enum, Model


class EquityGeneralMenu(Enum):
    EQUITY = "Equity 🏦"


class Equity(Model):
    id: int
    currency: str
    value: Decimal
