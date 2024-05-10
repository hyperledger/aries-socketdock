"""Backend interface for SocketDock."""

from abc import ABC, abstractmethod
from typing import Dict, Union


class Backend(ABC):
    """Backend interface for SocketDock."""

    @abstractmethod
    async def socket_connected(
        self,
        connection_id: str,
        headers: Dict[str, str],
    ):
        """Handle new socket connections, with calback provided."""

    @abstractmethod
    async def inbound_socket_message(
        self,
        connection_id: str,
        message: Union[str, bytes],
    ):
        """Handle inbound socket message, with calback provided."""

    @abstractmethod
    async def socket_disconnected(self, connection_id: str):
        """Handle socket disconnected."""
