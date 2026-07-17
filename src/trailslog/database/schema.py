SCHEMA = """
CREATE TABLE IF NOT EXISTS raw_telegram_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    telegram_message_id INTEGER NOT NULL UNIQUE,
    telegram_update_id  INTEGER UNIQUE,

    chat_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,

    is_bot INTEGER NOT NULL DEFAULT 0,

    message_date INTEGER NOT NULL,
    received_at INTEGER NOT NULL,

    -- Telegram reply chain.
    --
    -- Telegram bot replies are inconsistent:
    --
    -- - private chat: bot messages are NOT Telegram replies;
    -- - group chat:   bot messages ARE Telegram replies.
    --
    -- TrailsLog normalizes this behaviour by storing bot messages as
    -- replies in both cases. This field is therefore used both as the
    -- original Telegram reply chain and as the logical conversation
    -- chain used to reconstruct records.
    reply_to_message_id INTEGER,

    text TEXT NOT NULL,
    raw_json TEXT
);
"""
