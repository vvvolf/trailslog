from pathlib import Path
import shutil
from dataclasses import dataclass

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from trailslog.config import DATA_DIR

DEFAULT_FILE = Path("config/goals.example.toml")
USER_FILE = DATA_DIR / "goals.toml"


def ensure_goals_file() -> None:
    if USER_FILE.exists():
        return

    shutil.copy2(DEFAULT_FILE, USER_FILE)


def load_goals():

    with USER_FILE.open("rb") as f:
        data = tomllib.load(f)

    return {
        item["id"]: Goal(
            **item
        )
        for item in data["goal"]
    }


@dataclass
class Goal:

    id: str

    required: list[str]

    success_message: str

    failure_message: str


ensure_goals_file()

GOALS = load_goals()
