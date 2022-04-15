from shared.collections import Model


class Configuration(Model):
    id: int
    key: str
    value: str
