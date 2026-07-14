from telegram import Update
from telegram.ext import ContextTypes

from trailslog.activities import ACTIVITIES
from trailslog.database.database import save_raw_message

from trailslog.reports import build_today_report


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    await update.message.reply_text(
        "👋 Hi! Press or write /"
    )


async def command_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    save_raw_message(update)

    command = update.message.text.split()[0][1:]

    label = ACTIVITIES.get(command, command)

    await update.message.reply_text(
        f"""
✅ ({label}) — saved!
Want to save details? Reply to this message.
Made a mistake? Just reply with DEL or -.

✅ Готово!
Хочешь записать подробности? Ответь на это сообщение.
Ошибся? Просто ответь DEL или -.
        """
    )
    

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    save_raw_message(update)

    await update.message.reply_text(
        """
✅ Saved!
Want to add extra details? Reply to this message.
Made a mistake? Just reply with DEL or -.

✅ Готово!
Есть ещё подробности? Ответь на это сообщение.
Ошибся? Просто ответь DEL или -.
        """
        )


async def report_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    report = build_today_report(
        update.effective_chat.id
    )

    await update.message.reply_text(report)
