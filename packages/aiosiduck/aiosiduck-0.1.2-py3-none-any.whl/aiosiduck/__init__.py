import asyncio
from aioquic.quic.configuration import QuicConfiguration
from aioquic.asyncio.client import connect
from .quic_client_protocol import QuicClientProtocol
from typing import Union
from typing import Deque
from aioquic.quic.events import StreamDataReceived

if anext is None:

    async def anext(ait):
        return await ait.__anext__()


class SiduckClient:
    def __init__(
        self,
        host: str,
        port: str,
        certificate: str,
        timeout: Union[int, None] = None,
        connect_timeout: Union[int, None] = None,
        **kwargs,
    ):
        """
        host: host of server
        port: port of server
        certificate: path of certificate file. If not set, no certificate will be used.
        timeout: timeout for request. If not set, no timeout will be used.
        connect_timeout: timeout for connect to server. If not set, no timeout will be used.
        kwargs: attrs of aioquic.quic.configuration.QuicConfiguration
        """
        self.host = host
        self.port = port
        self.certificate = certificate
        self.timeout = timeout
        self.connect_timeout = connect_timeout
        self.configuration = QuicConfiguration(is_client=True, alpn_protocols=["siduck"], **kwargs)
        if certificate:
            self.configuration.load_verify_locations(certificate)
        self.client: QuicClientProtocol = None
        self._connectGenerator = None

    async def _connect(self):
        async with connect(
            self.host, self.port, configuration=self.configuration, create_protocol=QuicClientProtocol
        ) as client:
            yield client
            client._quic.close()

    def pack_response(self, res: Union[Deque[StreamDataReceived], None]):
        data = None
        if res:
            data = b""
            try:
                while True:
                    sdr = res.popleft()
                    data += sdr.data
            except IndexError:
                pass
        return data

    async def request(self, data: bytes):
        if not self.client:
            self._connectGenerator = self._connect()
            self.client = await asyncio.wait_for(anext(self._connectGenerator), timeout=self.connect_timeout)
        res = await self.client.request(data, self.timeout)
        return self.pack_response(res)

    async def close(self):
        if self._connectGenerator:
            try:
                await anext(self._connectGenerator)
            except StopAsyncIteration:
                pass
            self._connectGenerator = None
