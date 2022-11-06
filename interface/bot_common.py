import telegram
import telegram.ext

from dataclasses import dataclass

import database.api

from common.instances import (
    Coordinates,
    Distance,
    EntityPreferences,
    EntityType,
    Entity,
    TransportStop,
    RentalPoint,
    Restaraunt,
)
from interface.strings import BotString


@dataclass
class Context:
    update: telegram.Update
    tg_context: telegram.ext.ContextTypes.DEFAULT_TYPE
    database_api: database.api.DatabaseApi


async def make_radius_request(context: Context) -> None:
    await context.update.message.reply_text("Send radius")


async def make_invalid_distance_response(context: Context) -> None:
    await context.update.message.reply_text("Invalid float format")


def make_entity_description(entity: Entity) -> str:
    if isinstance(entity, TransportStop):
        transport: TransportStop = entity
        return f"""<b>Type:</b> {transport.kind.value}"""

    elif isinstance(entity, RentalPoint):
        rental: RentalPoint = entity
        return f"""<b>Type:</b> {rental.kind.value}"""

    elif isinstance(entity, Restaraunt):
        rest: Restaraunt = entity

        veganity = (
            BotString.ENTITY_DESC_VEGAN.value
            if rest.is_vegan
            else (
                BotString.ENTITY_DESC_VEGETERIAN.value
                if rest.is_vegeterian
                else (
                    BotString.ENTITY_DESC_VEG_OPTIONS.value
                    if rest.has_vegan_options
                    else ""
                )
            )
        )

        is_bio = (
            BotString.ENTITY_DESC_HAS_VEG_OPTIONS.value
            if rest.is_bio
            else BotString.ENTITY_DESC_NO_VEG_OPTIONS.value
        )
        is_chain = (
            BotString.ENTITY_IS_A_CHAIN.value
            if rest.is_chain
            else BotString.ENTITY_IS_NOT_A_CHAIN.value
        )

        return f"""  - {is_bio}
  - {is_chain}
  - {veganity}
"""


async def make_decide_response(
    context: Context, coordinates: Coordinates, radius: Distance
) -> None:
    for location_rank, location_and_desc in enumerate(
        context.database_api.get_best_locations(coordinates, radius, 5, 10)
    ):
        location, description = location_and_desc
        await context.update.message.reply_html(
            BotString.TOP_LOCATION.value.format(
                location_rank + 1, description.score, description.desc
            )
        )
        await context.update.message.reply_location(
            location.coord.lat, location.coord.lon
        )


async def make_overall_response(
    context: Context, coordinates: Coordinates, radius: Distance
) -> None:
    description = context.database_api.evaluate_region(coordinates, radius)

    await context.update.message.reply_html(
        BotString.REGION_DESCRIPTION.value.format(description.score, description.desc)
    )


async def make_inplace_response(
    context: Context,
    coordinates: Coordinates,
    radius: Distance,
    preferences: EntityPreferences,
) -> None:
    for entity_rank, entity_description in enumerate(
        context.database_api.get_best_entites(coordinates, radius, 5, preferences)
    ):
        entity, description = entity_description
        await context.update.message.reply_html(
            BotString.TOP_ENTITY.value.format(
                entity.name(),
                description.score,
                make_entity_description(entity),
                description.desc,
            )
        )
        await context.update.message.reply_location(
            entity.coords.lat, entity.coords.lon
        )


def markup_with_location() -> telegram.ReplyKeyboardMarkup:
    return telegram.ReplyKeyboardMarkup(
        keyboard=[],
        one_time_keyboard=True,
    )


def markup_helpful() -> telegram.ReplyKeyboardRemove:
    return telegram.ReplyKeyboardRemove()


def markup_distance() -> telegram.ReplyKeyboardMarkup:
    return telegram.ReplyKeyboardMarkup(
        keyboard=[],
        input_field_placeholder="Radius in km",
        one_time_keyboard=True,
    )


def markup_entity_kind() -> telegram.ReplyKeyboardMarkup:
    return telegram.ReplyKeyboardMarkup(
        keyboard=[list(map(lambda t: t.value, list(EntityType)))],
        one_time_keyboard=True,
        resize_keyboard=True,
    )
