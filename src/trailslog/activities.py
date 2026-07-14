from pathlib import Path
import shutil

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from telegram import BotCommand

from trailslog.config import DATA_DIR


DEFAULT_FILE = Path("config/activities.example.toml")
USER_FILE = DATA_DIR / "activities.toml"


def ensure_activities_file() -> None:
    if USER_FILE.exists():
        return

    shutil.copy2(DEFAULT_FILE, USER_FILE)


def load_activities() -> dict[str, str]:
    with USER_FILE.open("rb") as f:
        data = tomllib.load(f)

    return {
        item["command"]: item["label"]
        for item in data["activity"]
    }


ensure_activities_file()
ACTIVITIES = load_activities()


BOT_COMMANDS = [
    BotCommand(command, label)
    for command, label in ACTIVITIES.items()
]
