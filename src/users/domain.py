from shared.domain import Model


class UsersError(Exception):
    def __init__(self, message: str | None = None, *args, **kwargs) -> None:
        message = message or "Can not find user"
        super().__init__(message, *args, **kwargs)


class User(Model):
    id: int
    account_id: int
    chat_id: int
    username: str
    full_name: str

    def __hash__(self):
        return self.id
