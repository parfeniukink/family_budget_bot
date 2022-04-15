from typing import Union

from config import database
from costs.models import Cost
from equity.models import Equity
from incomes import Income


class EquityService:
    EQUITY_TABLE = "equity"

    @classmethod
    def update(cls, instance: Union[Cost, Income]) -> Equity:
        operation = "-" if isinstance(instance, Cost) else "+"
        q = f"UPDATE {cls.EQUITY_TABLE} SET value=value{operation}{instance.value} WHERE currency='{instance.currency}'"

        columns, execution_data = database.raw_execute(q)

        data = {k: v for k, v in zip(columns, execution_data)}
        return Equity(**data)
