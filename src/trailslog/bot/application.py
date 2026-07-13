from telegram.ext import Application, CommandHandler
from telegram.request import HTTPXRequest

from trailslog.bot.handlers import start
from trailslog.config import BOT_TOKEN
from trailslog.config import USE_PROXY
from trailslog.config import PROXY_URL


def create_application() -> Application:
    if USE_PROXY and not PROXY_URL:
        raise RuntimeError(
            "USE_PROXY=true, but PROXY_URL is empty."
        )

    builder = Application.builder().token(BOT_TOKEN)

    if USE_PROXY:
        request = HTTPXRequest(proxy=PROXY_URL)
        updates_request = HTTPXRequest(proxy=PROXY_URL)
        builder.request(request)
        builder.get_updates_request(updates_request)

    application = builder.build()
    
    application.add_handler(CommandHandler("start", start))

    return application