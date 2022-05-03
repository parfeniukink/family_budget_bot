from decimal import Decimal

from db import database
from equity.domain import Equity, EquityGeneralMenu
from finances import Currencies, Operations
from shared.formatting import get_number_in_frames
from shared.messages import LINE_ITEM


class EquityCRUD:
    __TABLE = "equity"

    @classmethod
    def get_formatted(cls) -> str:
        data = database.fetchall(cls.__TABLE)
        equity_all = (Equity(**d) for d in data)

        fequity = "\n".join(
            (
                LINE_ITEM.format(key=getattr(Currencies, e.currency.upper()).value, value=get_number_in_frames(e.value))
                for e in equity_all
            )
        )
        result = "\n\n".join((EquityGeneralMenu.EQUITY.value, fequity))

        return result

    @classmethod
    def update(cls, *_, operation: Operations, value: Decimal, currency: str) -> Equity:
        op = operation.value if operation is Operations.SUBTRACT else Operations.ADD.value
        q = f"UPDATE {cls.__TABLE} SET value=value{op}{value} " f"WHERE currency='{currency}' RETURNING *"

        data = database.raw_execute(q)[0]
        return Equity(**data)
