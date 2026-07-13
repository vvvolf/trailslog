from trailslog.app import ensure_runtime_dirs
from trailslog.bot.application import create_application

from trailslog.config import USE_PROXY
from trailslog.config import PROXY_URL

from trailslog.database.database import init_database

import logging

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

def main() -> None:
    ensure_runtime_dirs()

    init_database()

    application = create_application()

    print("TrailsLog started.")

    if USE_PROXY:
        print(f"Using proxy: {PROXY_URL}")
    else:
        print("Using direct connection")

    application.run_polling()
