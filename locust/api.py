

from sanic import Blueprint, Request, Websocket, json, text
import time
import sys

LAUNCH_TIME = time.time_ns()

api = Blueprint("api", url_prefix="/")


@api.get("/status")
async def status_handler(request: Request):
    """Return status information about the server."""
    uptime = time.time_ns() - LAUNCH_TIME
    return json(
        {
            "uptime": {
                "ns": uptime,
                "seconds": int(uptime / 1000000000),  # ns -> second conversion
            }
        }
    )

@api.post("/connect")
async def handle_connect(request: Request):
    print(request.body, file=sys.stderr)
    return json({})

@api.post("/message")
async def handle_message(request: Request):
    #print(request.body, file=sys.stderr)
    # We don't do anything with incoming message
    return json({})

@api.post("/disconnect")
async def handle_disconnect(request: Request):
    # We don't do anything with the disconnect
    print(request.body, file=sys.stderr)
    return json({})

