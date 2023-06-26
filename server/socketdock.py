import time
import logging
import argparse
from sanic import Request, Sanic, Websocket, text, json


from testbackend import TestBackend
from httpbackend import HTTPBackend

parser = argparse.ArgumentParser(
    prog="SocketDock", description="Socket Gateway for Configurable backends"
)
parser.add_argument("--bindip", default="127.0.0.1")
parser.add_argument("--bindport", default=8765)
parser.add_argument("--externalhostandport", default="127.0.0.1:8765")
parser.add_argument("--backend", default="loopback", choices=["loopback", "http"])
parser.add_argument("--message_uri")
parser.add_argument("--disconnect_uri")

args = parser.parse_args()

if args.backend == "loopback":
    backend = TestBackend()
elif args.backend == "http":
    backend = HTTPBackend(args.message_uri, args.disconnect_uri)

app = Sanic("SocketDock")

launchtime = time.time_ns()

app.config.WEBSOCKET_MAX_SIZE = 2**22
app.config.LOGGING = True

logging.basicConfig(level=logging.INFO)

# TODO: track timestamp of connections when connected
activeconnections = {}
lifetimeconnections = 0


@app.get("/status")
async def status_handler(request):
    uptime = (time.time_ns() - launchtime)
    return json({
        "uptime": {
            "ns": uptime,
            "seconds": int(uptime / 1000000000),  # ns -> second conversion
        },
        "connections": {
            "active": len(activeconnections),
            "lifetime": lifetimeconnections,
        },
    })


@app.post("/socket/<connectionid>/send")
async def socket_send(request, connectionid):
    logging.info(f"inbound message for {connectionid}")
    logging.info(f"Existing connections: {', '.join(activeconnections.keys())}")

    if connectionid not in activeconnections:
        return text("FAIL", status=500)

    socket = activeconnections[connectionid]
    await socket.send(request.body.decode('utf-8'))
    return text("OK")


@app.websocket("/ws")
async def socket_handler(request: Request, websocket: Websocket):
    global lifetimeconnections
    try:
        # register user
        logging.info("new client connected")
        socket_id = websocket.connection.id.hex
        activeconnections[socket_id] = websocket
        lifetimeconnections += 1
        logging.info(f"Existing connections: {', '.join(activeconnections.keys())}")
        logging.info(f"added connection {socket_id}")

        async for message in websocket:
            await backend.inbound_socket_message(
                {
                    "connection_id": socket_id,
                    "send": f"http://{args.externalhostandport}/socket/{socket_id}/send",
                },
                message,
            )

    finally:
        # unregister user
        del activeconnections[socket_id]
        logging.info(f"removed connection {socket_id}")
        await backend.socket_disconnected({"connection_id": socket_id})


# Note: This needs to run as a single process to maintain the context between the
# activeconnections structure and the connected sockets. This needs to be clustered _externally_
# in order to scale beyond the capability of a single instance.

if __name__ == "__main__":
    app.run(host=args.bindip, port=args.bindport, single_process=True)
