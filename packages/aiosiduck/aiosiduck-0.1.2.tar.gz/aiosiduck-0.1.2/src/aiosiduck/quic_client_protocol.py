import asyncio
from aioquic.asyncio import QuicConnectionProtocol
from aioquic.quic.events import QuicEvent, StreamDataReceived
from collections import deque
from typing import Deque, Dict


class QuicClientProtocol(QuicConnectionProtocol):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._request_events: Dict[int, Deque[QuicEvent]] = {}
        self._request_waiter: Dict[int, asyncio.Future[Deque[QuicEvent]]] = {}

    def quic_event_received(self, event: QuicEvent) -> None:
        if isinstance(event, StreamDataReceived):
            stream_id = event.stream_id
            self._request_events[event.stream_id].append(event)
            if event.end_stream:
                request_waiter = self._request_waiter.pop(stream_id)
                request_waiter.set_result(self._request_events.pop(stream_id))

    async def request(self, data: bytes, timeout=60) -> Deque[QuicEvent]:
        stream_id = self._quic.get_next_available_stream_id()
        self._quic.send_stream_data(stream_id=stream_id, data=data, end_stream=True)
        waiter = self._loop.create_future()
        self._request_events[stream_id] = deque()
        self._request_waiter[stream_id] = waiter
        self.transmit()
        return await asyncio.wait_for(waiter, timeout=timeout)
        # try:
        #     return await asyncio.wait_for(waiter, timeout=timeout)
        # except asyncio.exceptions.TimeoutError:
        #     pass
