from telegram import BotCommand
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import filters
from telegram.request import HTTPXRequest

from trailslog.bot.handlers import start
from trailslog.bot.handlers import command_handler
from trailslog.bot.handlers import text_handler
from trailslog.bot.handlers import report_handler
from trailslog.activities import ACTIVITIES
from trailslog.activities import BOT_COMMANDS
from trailslog.config import BOT_TOKEN
from trailslog.config import USE_PROXY
from trailslog.config import PROXY_URL


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(
        [
            BotCommand(cmd, desc)
            for cmd, desc in ACTIVITIES.items()
        ]
    )


def create_application() -> Application:
    if USE_PROXY and not PROXY_URL:
        raise RuntimeError(
            "USE_PROXY=true, but PROXY_URL is empty."
        )

    builder = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
    )

    if USE_PROXY:
        request = HTTPXRequest(proxy=PROXY_URL)
        updates_request = HTTPXRequest(proxy=PROXY_URL)

        builder.request(request)
        builder.get_updates_request(updates_request)

    application = builder.build()
    
    application.add_handler(CommandHandler("start", start))

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler,
        )
    )

    application.add_handler(
        CommandHandler(
            "report",
            report_handler,
        )
    )

    for command in ACTIVITIES:
        application.add_handler(
            CommandHandler(command, command_handler)
        )

    return application
