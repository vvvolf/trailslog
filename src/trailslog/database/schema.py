SCHEMA = """
CREATE TABLE IF NOT EXISTS raw_telegram_messages (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,

    telegram_update_id  INTEGER NOT NULL UNIQUE,
    telegram_message_id INTEGER NOT NULL,

    chat_id             INTEGER NOT NULL,
    user_id             INTEGER NOT NULL,

    message_date        INTEGER NOT NULL,
    received_at         INTEGER NOT NULL,

    reply_to_message_id INTEGER,

    text                TEXT NOT NULL,
    raw_json            TEXT NOT NULL
);
"""
