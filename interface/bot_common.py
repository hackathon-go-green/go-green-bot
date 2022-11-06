import telegram
import telegram.ext

from dataclasses import dataclass
from common.instances import Coordinates, Distance
from interface.strings import BotString


@dataclass
class Context:
    update: telegram.Update
    tg_context: telegram.ext.ContextTypes.DEFAULT_TYPE


async def make_radius_request(context: Context) -> None:
    await context.update.message.reply_text("Send radius")


async def make_invalid_distance_response(context: Context) -> None:
    await context.update.message.reply_text("Invalid float format")


async def make_decide_response(
    context: Context, coordinates: Coordinates, radius: Distance
) -> None:
    # TODO
    await context.update.message.reply_text(
        f"Do you actually want to go outside of your home? From {coordinates}, {radius}",
        reply_markup=markup_helpful(),
    )


async def make_overall_response(
    context: Context, coordinates: Coordinates, radius: Distance
) -> None:
    # TODO
    await context.update.message.reply_text(
        f"Do you actually want to go there? This shithole?? {coordinates}, {radius}",
        reply_markup=markup_helpful(),
    )


async def make_inplace_response(
    context: Context, coordinates: Coordinates, radius: Distance
) -> None:
    # TODO
    await context.update.message.reply_text(
        f"Go somewhere from {coordinates}, {radius}",
        reply_markup=markup_helpful(),
    )


def markup_with_location() -> telegram.ReplyKeyboardMarkup:
    return telegram.ReplyKeyboardMarkup(
        keyboard=[],
        one_time_keyboard=True,
    )


def markup_helpful() -> telegram.ReplyKeyboardMarkup:
    return telegram.ReplyKeyboardMarkup(
        keyboard=[],
        input_field_placeholder="Be Sustainable!",
        one_time_keyboard=True,
    )


def markup_distance() -> telegram.ReplyKeyboardMarkup:
    return telegram.ReplyKeyboardMarkup(
        keyboard=[],
        input_field_placeholder="Radius in km",
        one_time_keyboard=True,
    )
