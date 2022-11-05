import typing as t
import logging

from dataclasses import dataclass

import interface.state as state

from interface.bot_common import Context


class UserContext:
    def __init__(self):
        self.state: state.State = state.IdleState()

    async def on_command(self, context: Context, init_state: state.State) -> None:
        self.state = init_state
        logging.info(f"on_command, {type(self.state)}")
        await self.state.on_init(context)

    async def on_text(self, context: Context) -> None:
        next_state = await self.state.on_text(context)
        self.state = next_state if next_state is not None else state.IdleState()

    async def on_location(self, context: Context) -> None:
        next_state = await self.state.on_location(context)
        self.state = next_state if next_state is not None else state.IdleState()
