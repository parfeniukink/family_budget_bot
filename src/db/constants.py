from pathlib import Path

from shared.collections import Enum

SCRIPTS_FOLDER = Path(__file__).parent.parent.parent / "scripts/db"


class DB_ENGINES(Enum):
    POSTGRES = "postgresql"
    SQLITE = "sqlite"


DB_REGEX = (
    r"^(?P<db_engine>.*):\/\/((?P<db_username>[^:]*):(?P<db_password>[^@]*)@"
    r"(?P<db_hostname>[^:/]*)(:(?P<db_port>\d+))?\/)?(?P<db_name>.*)$"
)
