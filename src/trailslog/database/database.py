import json
import sqlite3
import time
from collections import defaultdict
from typing import Optional

from telegram import Update
from telegram import Message

from trailslog.config import DATA_DIR
from trailslog.database.schema import SCHEMA
from trailslog.models import Block


DB_PATH = DATA_DIR / "trailslog.db"


def init_database() -> None:
    with sqlite3.connect(DB_PATH) as connection:
        connection.executescript(SCHEMA)


def save_message(
    message: Message,
    *,
    is_bot: bool,
    telegram_update_id: Optional[int] = None,
    raw_json: Optional[str] = None,
    reply_to_message_id: Optional[int] = None,
):

    if message.text is None:
        return

    if reply_to_message_id is None and message.reply_to_message:
        reply_to_message_id = message.reply_to_message.message_id

    with sqlite3.connect(DB_PATH) as connection:

        connection.execute(
            """
            INSERT INTO raw_telegram_messages (

                telegram_message_id,
                telegram_update_id,

                chat_id,
                user_id,

                is_bot,

                message_date,
                received_at,

                reply_to_message_id,

                text,
                raw_json

            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                message.message_id,
                telegram_update_id,

                message.chat.id,
                message.from_user.id,

                int(is_bot),

                int(message.date.timestamp()),
                int(time.time()),

                reply_to_message_id,

                message.text,
                raw_json,
            ),
        )


def save_raw_message(update: Update):

    if update.message is None:
        return

    save_message(
        update.message,
        is_bot=False,
        telegram_update_id=update.update_id,
        raw_json=json.dumps(
            update.to_dict(),
            ensure_ascii=False,
        ),
    )


def get_all_messages(chat_id: int):

    with sqlite3.connect(DB_PATH) as connection:

        connection.row_factory = sqlite3.Row

        cursor = connection.execute(
            """
            SELECT *
            FROM raw_telegram_messages
            WHERE chat_id = ?
            ORDER BY message_date
            """,
            (chat_id,),
        )

        return cursor.fetchall()


def get_root_records_for_period(
    chat_id: int,
    user_id: int,
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
              AND user_id = ?
              AND message_date >= ?
              AND message_date < ?
              AND reply_to_message_id IS NULL
            ORDER BY message_date
            """,
            (
                chat_id,
                user_id,
                date_from,
                date_to,
            ),
        )

        return cursor.fetchall()


def get_record(
    chat_id: int,
    root_message_id: int,
) -> Block:

    rows = get_all_messages(chat_id)

    messages = {}

    children = defaultdict(list)

    for row in rows:
        block = Block(row=row)

        messages[
            row["telegram_message_id"]
        ] = block

        parent = row["reply_to_message_id"]

        if parent is not None:

            children[parent].append(block)

    def build(message_id: int) -> Block:

        block = messages[message_id]

        block.children = [
            build(child.row["telegram_message_id"])
            for child in children.get(message_id, [])
        ]

        return block
    
    return build(root_message_id)
