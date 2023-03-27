from backend import Backend
import aiohttp
import asyncio
class HTTPBackend(Backend):
    
    def __init__(self, message_uri, disconnect_uri):
        self._message_uri = message_uri
        self._disconnect_uri = disconnect_uri
    
    async def inbound_socket_message(self, callback_uris: dict, message: str):
        
        http_body = {
            "meta": dict,
            "message": message
        }

        send_uri = callback_uris['send']
        async with aiohttp.ClientSession() as session:
            async with session.post(self._message_uri, data=http_body) as resp:
                response = await resp.text()
                print(response)

        #response = requests.post(send_uri, data="Hello yourself!")
        
    async def socket_disconnected(self, bundle: dict):
        async with aiohttp.ClientSession() as session:
            async with session.post(self._disconnect_uri, data=bundle) as resp:
                response = await resp.text()
                print(response)
        
