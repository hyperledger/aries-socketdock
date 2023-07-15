"""Backend interface for SocketDock."""

from abc import ABC, abstractmethod
from typing import Union


class Backend(ABC):
    """Backend interface for SocketDock."""

    @abstractmethod
    async def inbound_socket_message(
        self, callback_uris: dict, message: Union[str, bytes]
    ):
        """Handle inbound socket message, with calback provided."""
        raise NotImplementedError()

    @abstractmethod
    async def socket_disconnected(self, bundle: dict):
        """Handle socket disconnected."""
        raise NotImplementedError()
