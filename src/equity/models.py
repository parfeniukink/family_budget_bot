from shared.collections import Model


class Equity(Model):
    id: int
    currency: str
    value: str
