import sqlite3

from trailslog.config import DATA_DIR
from trailslog.database.schema import SCHEMA


DB_PATH = DATA_DIR / "trailslog.db"


def init_database() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        connection.executescript(SCHEMA)
        