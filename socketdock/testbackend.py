"""Test backend for SocketDock."""

from typing import Dict, Union
import aiohttp

from .backend import Backend


class TestBackend(Backend):
    """Test backend for SocketDock."""

    def __init__(self, base_uri: str):
        """Initialize backend."""
        self.base_uri = base_uri

    async def socket_connected(
        self,
        connection_id: str,
        headers: Dict[str, str],
    ):
        """Socket connected.

        This test backend doesn't care, but can be useful to clean up state.
        """

    async def inbound_socket_message(
        self,
        connection_id: str,
        message: Union[str, bytes],
    ):
        """Receive socket message."""
        send_uri = f"{self.base_uri}/{connection_id}/send"
        async with aiohttp.ClientSession() as session:
            async with session.post(send_uri, data="Hello yourself") as resp:
                response = await resp.text()
                print(response)

    async def socket_disconnected(self, connection_id: str):
        """Socket disconnected.

        This test backend doesn't care, but can be useful to clean up state.
        """
