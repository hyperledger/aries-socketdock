import asyncio
import websockets


async def hello():
    async with websockets.connect("ws://localhost:8765/ws") as websocket:
        for i in range(5):
            print(f"> Hello world! ({i})", flush=True)
            await websocket.send(f"Hello world! ({i})")
            response = await websocket.recv()
            print(f"< {response}", flush=True)


asyncio.run(hello())
