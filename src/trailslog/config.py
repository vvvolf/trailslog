from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

DB_PATH = DATA_DIR / "trailslog.db"

BOT_TOKEN = os.environ["BOT_TOKEN"]

USE_PROXY = os.environ["USE_PROXY"] == "true"

PROXY_URL = os.environ["PROXY_URL"]
