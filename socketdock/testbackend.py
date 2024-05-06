"""Test backend for SocketDock."""

from typing import Union
import aiohttp

from .backend import Backend


class TestBackend(Backend):
    """Test backend for SocketDock."""

    async def socket_connected(self, callback_uris: dict):
        # This test method doesn't care, but can be useful to clean up state.
        pass

    async def inbound_socket_message(
        self, callback_uris: dict, message: Union[str, bytes]
    ):
        # send three backend messages in response
        # TODO: send response message via callback URI for sending a message
        send_uri = callback_uris["send"]
        async with aiohttp.ClientSession() as session:
            async with session.post(send_uri, data="Hello yourself") as resp:
                response = await resp.text()
                print(response)

        # response = requests.post(send_uri, data="Hello yourself!")

    async def socket_disconnected(self, bundle: dict):
        # This test method doesn't care, but can be useful to clean up state.
        pass
