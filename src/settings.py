from pathlib import Path
from typing import Any

from env import Env

ROOT_FOLDER = Path(__file__).parent.parent

DATABASE_URL = Env.database_url("DATABASE_URL")

DEFAULT_SEND_SETTINGS: dict[str, Any] = {"parse_mode": "HTML"}

RESTART_BUTTON_TEXT: str = "/restart"
ALLOWED_USER_ACCOUNT_IDS: list = Env.list("USERS_ACL")

DATES_KEYBOARD_LEN: int = Env.int("DATES_KEYBOARD_LEN", default=10)
