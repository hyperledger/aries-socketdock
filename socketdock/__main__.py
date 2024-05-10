"""Run the SocketDock server."""

import logging
import argparse
from sanic import Sanic

from .api import api, backend_var


def config() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="SocketDock", description="Socket Gateway for configurable backends"
    )
    parser.add_argument("--bindip", default="127.0.0.1")
    parser.add_argument("--bindport", default=8765)
    parser.add_argument("--endpoint", default="http://127.0.0.1:8765")
    parser.add_argument("--backend", default="loopback", choices=["loopback", "http"])
    parser.add_argument("--message-uri")
    parser.add_argument("--disconnect-uri")
    parser.add_argument("--connect-uri")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )

    return parser.parse_args()


def main():
    """Run the SocketDock server."""
    args = config()
    if args.backend == "loopback":
        from .testbackend import TestBackend

        backend = TestBackend(args.endpoint)
    elif args.backend == "http":
        from .httpbackend import HTTPBackend

        backend = HTTPBackend(
            args.endpoint, args.connect_uri, args.message_uri, args.disconnect_uri
        )
    else:
        raise ValueError("Invalid backend type")

    backend_var.set(backend)

    logging.basicConfig(level=args.log_level)

    app = Sanic("SocketDock")
    app.config.WEBSOCKET_MAX_SIZE = 2**22
    app.config.LOGGING = True
    app.blueprint(api)

    # Note: This needs to run as a single process to maintain the context
    # between the active_connections structure and the connected sockets. This
    # needs to be clustered _externally_ in order to scale beyond the
    # capability of a single instance.
    app.run(host=args.bindip, port=args.bindport, single_process=True)


if __name__ == "__main__":
    main()
