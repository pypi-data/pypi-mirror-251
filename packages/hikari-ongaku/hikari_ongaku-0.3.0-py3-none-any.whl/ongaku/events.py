from __future__ import annotations

import logging
import typing as t

from .errors import (
    SessionStartException,
)
from .abc import (
    ReadyEvent,
    StatisticsEvent,
    TrackEndEvent,
    TrackExceptionEvent,
    TrackStartEvent,
    TrackStuckEvent,
    WebsocketClosedEvent,
)

if t.TYPE_CHECKING:
    from .node import Node

INTERNAL_LOGGER = logging.getLogger(__name__)


class EventHandler:
    def __init__(self, node: Node) -> None:
        self._node = node

    async def handle_payload(self, payload: dict[t.Any, t.Any]) -> None:
        try:
            op_code = payload["op"]
        except Exception as e:
            raise e

        if op_code == "ready":
            await self.ready_payload(payload)

        elif op_code == "stats":
            await self.stats_payload(payload)

        elif op_code == "event":
            await self.event_payload(payload)

        elif op_code == "playerUpdate":
            pass

        else:
            logging.warning(f"OP code not recognized: {op_code}")

    async def ready_payload(self, payload: dict[t.Any, t.Any]) -> None:
        try:
            session_id = str(payload["sessionId"])
        except Exception:
            raise SessionStartException("Session id does not exist in ready payload.")

        if session_id.strip() == "":
            raise SessionStartException("Session ID cannot be none.")

        self._node._internal.session_id = session_id

        try:
            event = ReadyEvent._from_payload(payload, app=self._node._ongaku.bot)
        except Exception as e:
            raise e

        INTERNAL_LOGGER.info("Successfully connected to the server.")
        await self._node._ongaku.bot.dispatch(event)

    async def stats_payload(self, payload: dict[t.Any, t.Any]) -> None:
        try:
            event = StatisticsEvent._from_payload(payload, app=self._node._ongaku.bot)
        except Exception as e:
            raise e

        await self._node._ongaku.bot.dispatch(event)

    async def event_payload(self, payload: dict[t.Any, t.Any]) -> None:
        try:
            event_type = payload["type"]
        except Exception as e:
            raise e

        if event_type == "TrackStartEvent":
            try:
                event = TrackStartEvent._from_payload(
                    payload, app=self._node._ongaku.bot
                )
            except Exception as e:
                raise e

        elif event_type == "TrackEndEvent":
            try:
                event = TrackEndEvent._from_payload(payload, app=self._node._ongaku.bot)
            except Exception as e:
                raise e

        elif event_type == "TrackExceptionEvent":
            try:
                event = TrackExceptionEvent._from_payload(
                    payload, app=self._node._ongaku.bot
                )
            except Exception as e:
                raise e

        elif event_type == "TrackStuckEvent":
            try:
                event = TrackStuckEvent._from_payload(
                    payload, app=self._node._ongaku.bot
                )
            except Exception as e:
                raise e

        elif event_type == "WebSocketClosedEvent":
            try:
                event = WebsocketClosedEvent._from_payload(
                    payload, app=self._node._ongaku.bot
                )
            except Exception as e:
                raise e

        else:
            return

        await self._node._ongaku.bot.dispatch(event)


# MIT License

# Copyright (c) 2023 MPlatypus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
