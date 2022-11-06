import typing as t
import telegram
import logging

from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

import interface.state as state

from interface.bot_common import (
    Context,
    markup_helpful,
)
from interface.user_context import UserContext
from interface.strings import BotString


class Bot:
    def __init__(self):
        self.user_contexts: t.Dict[int, UserContext] = {}

    def get_user_context(self, user: telegram.User) -> UserContext:
        if user.id not in self.user_contexts:
            self.user_contexts[user.id] = UserContext()
        return self.user_contexts[user.id]

    async def on_start(
        self, update: telegram.Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user
        if user is None:
            return
        await update.message.reply_html(
            BotString.START.value.format(user.first_name),
            reply_markup=markup_helpful(),
        )

    async def on_help(
        self, update: telegram.Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        await update.message.reply_html(
            BotString.HELP.value, reply_markup=markup_helpful()
        )

    async def on_decide(
        self, update: telegram.Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user
        if user is None:
            return
        logging.info(f"Handle command /decide from user {user}")
        await self.get_user_context(user).on_command(
            Context(update, context), state.DecideCommandState()
        )

    async def on_inplace(
        self, update: telegram.Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user
        if user is None:
            return
        logging.info(f"Handle command /inplace from user {user}")
        await self.get_user_context(user).on_command(
            Context(update, context), state.InPlaceCommandState()
        )

    async def on_overall(
        self, update: telegram.Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user
        if user is None:
            return
        logging.info(f"Handle command /overall from user {user}")
        await self.get_user_context(user).on_command(
            Context(update, context), state.OverallCommandState()
        )

    async def on_text(
        self, update: telegram.Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user
        if user is None:
            return
        logging.info(f"Handle text from user {user}")
        await self.get_user_context(user).on_text(Context(update, context))

    async def on_location(
        self, update: telegram.Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user
        if user is None:
            return
        logging.info(
            f"Handle location from user {user} {type(self.get_user_context(user).state)}"
        )
        await self.get_user_context(user).on_location(Context(update, context))

    def bind_with_application(self, application: Application) -> None:
        application.add_handler(CommandHandler("start", self.on_start))
        application.add_handler(CommandHandler("help", self.on_help))
        application.add_handler(CommandHandler("decide", self.on_decide))
        application.add_handler(CommandHandler("inplace", self.on_inplace))
        application.add_handler(CommandHandler("overall", self.on_overall))

        assert application.bot.set_my_commands(
            [
                ("help", BotString.COMMAND_DESC_HELP.value),
                ("decide", BotString.COMMAND_DESC_DECIDE.value),
                ("inplace", BotString.COMMAND_DESC_INPLACE.value),
                ("overall", BotString.COMMAND_DESC_OVERALL.value),
            ]
        )

        application.add_handler(MessageHandler(filters.TEXT, self.on_text))
        application.add_handler(MessageHandler(filters.LOCATION, self.on_location))

        logging.info("Binded to application")
