from shared.collections import Model


class User(Model):
    id: int
    account_id: int
    chat_id: int
    username: str
    full_name: str
