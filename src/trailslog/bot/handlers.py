from telegram import Update
from telegram.ext import ContextTypes

from trailslog.bot.commands import COMMANDS


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    await update.message.reply_text(
        "👋 Hello! I'm here! Начинай писать команды с /..."
    )


async def command_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    command = update.message.text.split()[0][1:]

    label = COMMANDS.get(command, command)

    await update.message.reply_text(
        f"✅ Saved: {label}"
    )
    