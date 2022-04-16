from typing import Optional

from shared.collections import Model


class Configuration(Model):
    id: int
    key: str
    value: Optional[str]
