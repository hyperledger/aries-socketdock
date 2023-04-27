import logging
from backend import Backend
import aiohttp


class HTTPBackend(Backend):
    def __init__(self, message_uri, disconnect_uri):
        self._message_uri = message_uri
        self._disconnect_uri = disconnect_uri

    async def inbound_socket_message(self, callback_uris: dict, message: str):
        http_body = {"meta": callback_uris, "message": message}

        # send_uri = callback_uris["send"]
        async with aiohttp.ClientSession() as session:
            logging.info(f"Posting message {http_body} to {self._message_uri}")
            async with session.post(self._message_uri, json=http_body) as resp:
                logging.info(resp)
                response = await resp.text()
                logging.info(response)

        # response = requests.post(send_uri, data="Hello yourself!")

    async def socket_disconnected(self, bundle: dict):
        async with aiohttp.ClientSession() as session:
            async with session.post(self._disconnect_uri, json=bundle) as resp:
                response = await resp.text()
                logging.info(response)
