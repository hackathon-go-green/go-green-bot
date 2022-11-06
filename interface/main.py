import logging
import interface.config as config
import telegram

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram.ext import (
    Application,
)

import interface.bot
import database.api

from pathlib import Path


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config.TEST_TOKEN).build()

    database_api = database.api.DatabaseApi(Path("database"))
    bot_logic = interface.bot.Bot(database_api)

    bot_logic.bind_with_application(application)
    logging.info("Run pooling")
    application.run_polling()


if __name__ == "__main__":
    main()
