import json
import sqlite3
import time

from telegram import Update

from trailslog.config import DATA_DIR
from trailslog.database.schema import SCHEMA


DB_PATH = DATA_DIR / "trailslog.db"


def init_database() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        connection.executescript(SCHEMA)


def save_raw_message(update: Update) -> None:
    message = update.message

    if message is None:
        return

    if message.text is None:
        return

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO raw_telegram_messages (
                telegram_update_id,
                telegram_message_id,
                chat_id,
                user_id,
                message_date,
                received_at,
                text,
                raw_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                update.update_id,
                message.message_id,
                message.chat.id,
                message.from_user.id,
                message.date.timestamp(),
                int(time.time()),
                message.text,
                json.dumps(
                    update.to_dict(),
                    ensure_ascii=False,
                ),
            ),
        )
        