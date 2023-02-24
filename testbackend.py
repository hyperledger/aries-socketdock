from backend import Backend
import aiohttp
import asyncio
class TestBackend(Backend):
    async def inbound_socket_message(self, callback_uris: dict, message: str):
        #send three backend messages in response
        #TODO: send response message via callback URI for sending a message
        send_uri = callback_uris['send']
        async with aiohttp.ClientSession() as session:
            async with session.post(send_uri, data="Hello yourself") as resp:
                response = await resp.text()
                print(response)

        #response = requests.post(send_uri, data="Hello yourself!")
        
    async def socket_disconnected(self, bundle: dict):
        #This test method doesn't care, but can be useful to clean up state.
        pass
        
