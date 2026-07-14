from telegram import Update
from telegram.ext import ContextTypes

from trailslog.bot.commands import COMMANDS
from trailslog.database.database import save_raw_message


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

    label = COMMANDS.get(command, command)

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
