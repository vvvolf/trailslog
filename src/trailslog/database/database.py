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

    reply_to_message_id = None

    if message.reply_to_message:
        reply_to_message_id = message.reply_to_message.message_id

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
                reply_to_message_id,
                text,
                raw_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                update.update_id,
                message.message_id,
                message.chat.id,
                message.from_user.id,
                message.date.timestamp(),
                int(time.time()),
                reply_to_message_id,
                message.text,
                json.dumps(
                    update.to_dict(),
                    ensure_ascii=False,
                ),
            ),
        )


def get_messages_for_date(
    chat_id: int,
    date_from: int,
    date_to: int,
):
    with sqlite3.connect(DB_PATH) as connection:

        connection.row_factory = sqlite3.Row

        cursor = connection.execute(
            """
            SELECT *
            FROM raw_telegram_messages
            WHERE chat_id = ?
              AND message_date >= ?
              AND message_date < ?
            ORDER BY message_date
            """,
            (
                chat_id,
                date_from,
                date_to,
            ),
        )

        return cursor.fetchall()
