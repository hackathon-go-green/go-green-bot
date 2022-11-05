import abc
import typing as t
import logging

from common.instances import Coordinates
from interface.strings import BotString
from interface.bot_common import (
    Context,
    make_radius_request,
    make_invalid_distance_response,
    make_decide_response,
    make_overall_response,
    make_inplace_response,
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


class DecideCommandState(State):
    def __init__(self):
        self.location: t.Optional[Coordinates] = None
        self.radius: t.Optional[float] = None

    async def on_init(self, context: Context) -> None:
        await context.update.message.reply_html(BotString.DECISION_LOCATION.value)

    async def on_text(self, context: Context) -> t.Optional["State"]:
        if self.location is None:
            await context.update.message.reply_html(
                BotString.INVALID_LOCATION_FORMAT.value
            )
            return self
        text = context.update.message.text
        try:
            self.radius = float(text)
            await make_decide_response(context, self.location, self.radius)
            return None
        except ValueError:
            await context.update.message.reply_html(
                BotString.INVALID_RADIUS_FORMAT.value
            )
            return self

    async def on_location(self, context: Context) -> t.Optional["State"]:
        if self.location is not None:
            await self.on_init(context)
            return self
        update_location = context.update.message.location
        self.location = Coordinates(update_location.latitude, update_location.longitude)
        await context.update.message.reply_html(BotString.DECISION_RADIUS.value)
        return self


class OverallCommandState(State):
    def __init__(self):
        self.location: t.Optional[Coordinates] = None
        self.radius: t.Optional[float] = None

    async def on_init(self, context: Context) -> None:
        await context.update.message.reply_html(BotString.OVERALL_LOCATION.value)

    async def on_text(self, context: Context) -> t.Optional["State"]:
        if self.location is None:
            await context.update.message.reply_html(
                BotString.INVALID_LOCATION_FORMAT.value
            )
            return self
        text = context.update.message.text
        try:
            self.radius = float(text)
            await make_overall_response(context, self.location, self.radius)
            return None
        except ValueError:
            await context.update.message.reply_html(
                BotString.INVALID_RADIUS_FORMAT.value
            )
            return self

    async def on_location(self, context: Context) -> t.Optional["State"]:
        if self.location is not None:
            await self.on_init(context)
            return self
        update_location = context.update.message.location
        self.location = Coordinates(update_location.latitude, update_location.longitude)
        await context.update.message.reply_html(BotString.OVERALL_RADIUS.value)
        return self


class InPlaceCommandState(State):
    def __init__(self):
        self.location: t.Optional[Coordinates] = None
        self.radius: t.Optional[float] = None

    async def on_init(self, context: Context) -> None:
        await context.update.message.reply_html(BotString.INPLACE_LOCATION.value)

    async def on_text(self, context: Context) -> t.Optional["State"]:
        if self.location is None:
            await context.update.message.reply_html(
                BotString.INVALID_LOCATION_FORMAT.value
            )
            return self
        text = context.update.message.text
        try:
            self.radius = float(text)
            await make_inplace_response(context, self.location, self.radius)
            return None
        except ValueError:
            await context.update.message.reply_html(
                BotString.INVALID_RADIUS_FORMAT.value
            )
            return self

    async def on_location(self, context: Context) -> t.Optional["State"]:
        if self.location is not None:
            await self.on_init(context)
            return self
        update_location = context.update.message.location
        self.location = Coordinates(update_location.latitude, update_location.longitude)
        await context.update.message.reply_html(BotString.INPLACE_RADIUS.value)
        return self
