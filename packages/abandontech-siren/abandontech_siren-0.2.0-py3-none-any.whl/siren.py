import asyncio
import struct

from dataclasses import dataclass

PADDING = b"\x00\x00"


@dataclass
class PacketTypes:
    """Dataclass to contain various packet types."""
    login: int = 3
    command: int = 2
    command_response: int = 0

    auth_failed = -1


class RconClient:
    """Manages minecraft RCON authentication and message sending."""

    def __init__(self, host: str, port: int, password: str):
        self.host = host
        self.port = port
        self.password = password

        self.is_authenticated = False

        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None

    async def __aenter__(self) -> "RconClient":
        """
        When an async context manager instantiates a class instance, create the reader and writer, then authenticate
        with the RCON server.
        """
        if not self._writer:
            self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
            await self.authenticate()

        return self
    
    async def __aexit__(self, *_) -> None:
        """When the async context manager exits, close the writer connection for the class instance."""
        if self._writer:
            self._writer.close()
    
    async def authenticate(self) -> None:
        """Send the login packet to the RCON server"""
        if not self.is_authenticated:
            await self._send(PacketTypes.login, self.password)
            self.is_authenticated = True
    
    async def _read_data(self, data_len: int) -> bytes:
        """Reads the next received packet based on the expected packet length"""
        data = b""
        
        while len(data) < data_len:
            data += await self._reader.read(data_len - len(data))
        
        return data
    
    async def _send(self, packet_type: int, message: str) -> str:
        """
        Sends a string to the RCON server with the given packet type.

        Valid packet types are defined as part of the PacketTypes dataclass.
        """
        if not self._writer:
            raise ConnectionError("Client is not connected. Ensure you are using an async context manager.")

        out_packet = struct.pack("<li", 0, packet_type) + message.encode("utf8") + PADDING
        out_packet_len = struct.pack("<i", len(out_packet))
        self._writer.write(out_packet_len + out_packet)

        in_packet_len = struct.unpack("<i", await self._read_data(4))
        in_packet = await self._read_data(in_packet_len[0])

        in_packet_id = struct.unpack("<ii", in_packet[:8])[0]
        in_data, in_padding = in_packet[8:-2], in_packet[-2:]

        if in_padding != PADDING:
            raise ValueError("Received packet was not well formed.")

        if in_packet_id == PacketTypes.auth_failed:
            raise ConnectionRefusedError("Invalid password")
        
        data = in_data.decode("utf8")

        return data

    async def send(self, command: str) -> str:
        """
        Send the given string to the RCON server as a command.

        command should be the full message to send to the server including trailing forward slash, i.e '/list'
        """
        result = await self._send(PacketTypes.command, command)

        # This sleep was added by the original author with a comment that there is no explanation.
        # I am leaving here incase we encounter strange issues, but the answer is almost certainly not to sleep here.
        # await asyncio.sleep(0.003)
        return result
