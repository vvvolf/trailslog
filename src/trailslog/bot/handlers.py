from telegram import Update
from telegram.ext import ContextTypes

from trailslog.activities import ACTIVITIES
from trailslog.database.database import save_raw_message
from trailslog.database.database import save_message

from trailslog.reports import build_today_report


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    sent = await update.message.reply_text(
        "👋 Hi! Press or write /"
    )


async def command_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    save_raw_message(update)

    command = update.message.text.split()[0][1:]

    label = ACTIVITIES.get(command, command)

    sent = await update.message.reply_text(
        f"""
✅ ({label}) — saved!
        """
    )

    save_message(
        sent,
        is_bot=True,
        reply_to_message_id=update.message.message_id,
    )


async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    save_raw_message(update)

    sent = await update.message.reply_text(
        """
✅ Saved extra!
        """
    )

    save_message(
        sent,
        is_bot=True,
        reply_to_message_id=update.message.message_id,
    )


async def report_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    report = build_today_report(
        update.effective_chat.id,
        update.message.from_user.id,
    )

    sent = await update.message.reply_text(report)
