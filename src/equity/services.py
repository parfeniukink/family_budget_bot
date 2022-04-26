from typing import Union

from config import database
from costs.models import Cost
from equity.models import Equity
from incomes import Income
from shared.finances import Currencies
from shared.strings import get_number_in_frames


class EquityService:
    TABLE = "equity"

    @classmethod
    def get_formatted(cls) -> str:
        data = database.fetchall(cls.TABLE)
        equity_all = (Equity(**d) for d in data)

        f_equity = "\n".join(
            (
                " ➙ ".join([getattr(Currencies, e.currency.upper()).value, get_number_in_frames(e.value)])
                for e in equity_all
            )
        )
        result = "\n\n".join(("Equity 🏦", f_equity))

        return result

    @classmethod
    def update(cls, instance: Union[Cost, Income]) -> Equity:
        operation = "-" if isinstance(instance, Cost) else "+"
        q = (
            f"UPDATE {cls.TABLE} SET value=value{operation}{instance.value} "
            f"WHERE currency='{instance.currency}' RETURNING *"
        )

        data = database.raw_execute(q)[0]
        return Equity(**data)
