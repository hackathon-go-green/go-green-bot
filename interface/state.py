import abc
import typing as t
import logging
import telegram

import interface.config as config

from common.instances import (
    Coordinates,
    EntityType,
    EntityPreferences,
)
from interface.strings import BotString
from interface.bot_common import (
    Context,
    make_radius_request,
    make_invalid_distance_response,
    make_decide_response,
    make_overall_response,
    make_inplace_response,
    markup_with_location,
    markup_distance,
    markup_entity_kind,
)


class State(abc.ABC):
    async def on_init(self, context: Context) -> None:
        pass

    async def on_text(self, context: Context) -> t.Optional["State"]:
        pass

    async def on_location(self, context: Context) -> t.Optional["State"]:
        pass


class IdleState(State):
    async def on_init(self, context: Context) -> None:
        return

    async def on_text(self, context: Context) -> t.Optional["State"]:
        return self

    async def on_location(self, context: Context) -> t.Optional["State"]:
        return self


def validate_radius(radius_repr: str) -> t.Optional[str]:
    try:
        radius = float(radius_repr)
        if radius < config.MIN_RADIUS:
            return BotString.INVALID_RADIUS_TOO_SMALL.value
        if radius > config.MAX_RADIUS:
            return BotString.INVALID_RADIUS_TOO_BIG.value
    except ValueError:
        return BotString.INVALID_RADIUS_FORMAT.value


class DecideCommandState(State):
    def __init__(self):
        self.location: t.Optional[Coordinates] = None
        self.radius: t.Optional[float] = None

    async def on_init(self, context: Context) -> None:
        await context.update.message.reply_html(
            BotString.DECISION_LOCATION.value, reply_markup=markup_with_location()
        )

    async def on_text(self, context: Context) -> t.Optional["State"]:
        if self.location is None:
            await context.update.message.reply_html(
                BotString.INVALID_LOCATION_FORMAT.value,
                reply_markup=markup_with_location(),
            )
            return self
        radius_repr = context.update.message.text
        radius_validation = validate_radius(radius_repr)
        if radius_validation is not None:
            await context.update.message.reply_html(
                radius_validation, reply_markup=markup_distance()
            )
            return self

        self.radius = float(radius_repr)
        await make_decide_response(context, self.location, self.radius)
        return None

    async def on_location(self, context: Context) -> t.Optional["State"]:
        if self.location is not None:
            await self.on_init(context)
            return self
        update_location = context.update.message.location
        self.location = Coordinates(update_location.latitude, update_location.longitude)
        await context.update.message.reply_html(
            BotString.DECISION_RADIUS.value,
            reply_markup=markup_distance(),
        )
        return self


class OverallCommandState(State):
    def __init__(self):
        self.location: t.Optional[Coordinates] = None
        self.radius: t.Optional[float] = None

    async def on_init(self, context: Context) -> None:
        await context.update.message.reply_html(
            BotString.OVERALL_LOCATION.value, reply_markup=markup_with_location()
        )

    async def on_text(self, context: Context) -> t.Optional["State"]:
        if self.location is None:
            await context.update.message.reply_html(
                BotString.INVALID_LOCATION_FORMAT.value,
                reply_markup=markup_with_location(),
            )
            return self

        radius_repr = context.update.message.text
        radius_validation = validate_radius(radius_repr)
        if radius_validation is not None:
            await context.update.message.reply_html(
                radius_validation, reply_markup=markup_distance()
            )
            return self

        self.radius = float(radius_repr)
        await make_overall_response(context, self.location, self.radius)
        return None

    async def on_location(self, context: Context) -> t.Optional["State"]:
        if self.location is not None:
            await self.on_init(context)
            return self
        update_location = context.update.message.location
        self.location = Coordinates(update_location.latitude, update_location.longitude)
        await context.update.message.reply_html(
            BotString.OVERALL_RADIUS.value,
            reply_markup=markup_distance(),
        )
        return self


class InPlaceCommandState(State):
    def __init__(self):
        self.location: t.Optional[Coordinates] = None
        self.radius: t.Optional[float] = None
        self.entity_kind: t.Optional[EntityType] = None

    async def on_init(self, context: Context) -> None:
        await context.update.message.reply_html(
            BotString.INPLACE_LOCATION.value, reply_markup=markup_with_location()
        )

    async def on_text(self, context: Context) -> t.Optional["State"]:
        if self.location is None:
            await context.update.message.reply_html(
                BotString.INVALID_LOCATION_FORMAT.value,
                reply_markup=markup_with_location(),
            )
            return self

        elif self.radius is None:
            radius_repr = context.update.message.text
            radius_validation = validate_radius(radius_repr)
            if radius_validation is not None:
                await context.update.message.reply_html(
                    radius_validation, reply_markup=markup_distance()
                )
                return self
            self.radius = float(radius_repr)
            await context.update.message.reply_html(
                BotString.INPLACE_ENTITY_KIND.value, reply_markup=markup_entity_kind()
            )
            return self

        else:
            entity_kind_repr = context.update.message.text

            kind_by_name = {
                EntityType.TRANSPORT.value: EntityType.TRANSPORT,
                EntityType.RESTARAUNT.value: EntityType.RESTARAUNT,
                EntityType.RENTAL_POINT.value: EntityType.RENTAL_POINT,
            }

            if entity_kind_repr not in kind_by_name:
                await context.update.message.reply_html(
                    BotString.INVALID_ENTITY_KIND.value,
                    reply_markup=markup_entity_kind(),
                )
                return self

            self.entity_kind = kind_by_name[entity_kind_repr]

            await make_inplace_response(
                context, self.location, self.radius, EntityPreferences(self.entity_kind)
            )
            return None

    async def on_location(self, context: Context) -> t.Optional["State"]:
        if self.location is not None:
            return
        update_location = context.update.message.location
        self.location = Coordinates(update_location.latitude, update_location.longitude)
        await context.update.message.reply_html(
            BotString.INPLACE_RADIUS.value,
            reply_markup=markup_distance(),
        )
        return self
