from __future__ import annotations

import asyncio
import enum
import random
import struct
from typing import Union


class PacketType(enum.Enum):
    LOGIN = 3
    COMMAND = 2
    RESPONSE = 0
    INVALID = 111


class Packet(bytearray):
    """A packet as defined in the Minecraft
    [RCON protocol](https://wiki.vg/RCON#Packet_Format).
    """

    def __init__(self, packet_data: Union[bytes, bytearray]) -> None:
        """`packet_data` must include length field"""
        if len(packet_data) > MAX_PAYLOAD_SIZE_IN + MIN_PACKET_SIZE:
            raise ValueError("invalid packet size, packet too long")
        if len(packet_data) < MIN_PACKET_SIZE:
            raise ValueError("invalid packet size, packet too short")
        if packet_data[-2:] != b"\x00\x00":
            raise ValueError("invalid packet, missing null-terminator")
        super().__init__(packet_data)

    @classmethod
    def from_payload(
        cls,
        payload: str,
        type: PacketType = PacketType.COMMAND,
        request_id: Union[int, None] = None,
    ) -> Packet:
        """Create a new packet with the given `type`, `payload` and `request_id`.

        :param payload: The payload of the packet.
        :type payload: str
        :param type: The type of the packet, defaults to `PacketType.COMMAND`
        :type type: PacketType, optional
        :param request_id: A custom request id, random if `None`, defaults to `None`
        :type request_id: int | None, optional
        :return: The new packet.
        :rtype: Packet
        """
        packet = cls(bytes(MIN_PACKET_SIZE))
        packet.payload = payload
        packet.type = type

        request_id = request_id or random.randint(-2147483648, 2147483647)
        assert -2147483648 <= request_id <= 2147483647
        packet.request_id = request_id

        return packet

    @property
    def length(self) -> int:
        """The value of the length field.
        (The length of the packet excluding the length field itself)
        """
        return len(self) - 4  # length field is not included

    @property
    def request_id(self) -> int:
        return struct.unpack("<i", self[4:8])[0]

    @request_id.setter
    def request_id(self, value: int) -> None:
        self[4:8] = struct.pack("<i", value)

    @property
    def type(self) -> PacketType:
        """The packet type.
        3: Login
        2: Command
        0: Response
        111: Invalid (to check for fragmentation)
        """
        return PacketType(struct.unpack("<i", self[8:12])[0])

    @type.setter
    def type(self, value: PacketType) -> None:
        self[8:12] = struct.pack("<i", value.value)

    @property
    def payload(self) -> str:
        """The payload of the packet, excluding the null-terminator.
        Usually a command or its response.
        """
        return self[12:-2].decode("utf-8")

    @payload.setter
    def payload(self, value: str) -> None:
        if len(value) > MAX_PAYLOAD_SIZE_OUT:
            raise ValueError("payload too long")
        self[12:-2] = value.encode("ascii")
        self[:4] = struct.pack("<i", self.length)

    def as_dict(self) -> dict:
        """Return a dict representation of the packet,
        including `length`, `request_id`, `type` and `payload`.
        """
        return {
            "length": self.length,
            "request_id": self.request_id,
            "type": self.type,
            "payload": self.payload,
        }

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in self.as_dict().items())})>"


MAX_PAYLOAD_SIZE_IN = 4096  # without null-terminator
MAX_PAYLOAD_SIZE_OUT = 1446  # without null-terminator
MIN_PACKET_SIZE = 14  # empty payload
MAX_PACKET_SIZE_IN = MAX_PAYLOAD_SIZE_IN + MIN_PACKET_SIZE


class Client:
    """An async Minecraft RCON client that supports
    [fragmented responses](https://wiki.vg/RCON#Fragmentation).

    `asycnio.gather()` is supported in theory, but does not work in practice
    until [MC-87863](https://bugs.mojang.com/browse/MC-87863) is fixed.
    """

    def __init__(self, host: str, password: str, port: int = 25575) -> None:
        """Initiate a new RCON client to send commands to a Minecraft server.

        Best used as an async context manager:
        ```py
        async with Client("myserver.com", "password") as client:
            await client.command("say Hello world")
        ```

        or call `connect` and `close` directly:
        ```py
        client = Client("myserver.com", "password")
        await client.connect()
        await client.command("say Hello world")
        await client.close()
        ```

        :param host: The hostname or ip of the server.
        :type host: str
        :param password: The RCON password you set in the server.properties
        :type password: str
        :param port: The RCON port you set in the server.properties, defaults to 25575
        :type port: int, optional
        """
        self.host = host
        self.port = port
        self.password = password

        self._reader: Union[asyncio.StreamReader, None] = None
        self._writer: Union[asyncio.StreamWriter, None] = None
        self._ready = False
        self._writing_queue: asyncio.Queue[Packet] = asyncio.Queue()
        self._waiting: dict[int, asyncio.Future[list[Packet]]] = {}

    @property
    def ready(self) -> bool:
        """Whether the client is ready to send commands"""
        return self._ready

    async def connect(self):
        """Sets up the connection between the client and server."""
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
        await self._login()
        self.__producer_task = asyncio.create_task(self.__producer())
        self.__consumer_task = asyncio.create_task(self.__consumer())
        self._ready = True

    async def command(self, command: str, timeout: Union[float, None] = 2) -> str:
        """Executes a command on the server.

        :param command: The command to send.
        :type command: str
        :param timeout: The time in seconds to wait for a response, defaults to `2`
        :type timeout: float | None, optional

        :raises asyncio.TimeoutError: If the response takes longer than `timeout`.

        :return: The response from the server.
        :rtype: str
        """
        packets = await self._send(
            Packet.from_payload(command.removeprefix("/")), timeout=timeout
        )
        response = "".join(packet.payload for packet in packets)
        return response

    async def _login(self):
        """Log in to the server using the password.

        :raises ValueError: If the password is invalid.
        :raises ValueError: If the server responds with an unknown request id.
        """
        request = Packet.from_payload(self.password, PacketType.LOGIN)
        self._writer.write(request)
        response = Packet(await self._reader.readexactly(MIN_PACKET_SIZE))

        if response.request_id == -1:
            raise ValueError(f"invalid rcon password for server {self.host}")
        elif response.request_id != request.request_id:
            raise ValueError("unknown response from server")

    async def __consumer(self):
        """Distributes recieved packets to the waiting futures and handles
        [fragmented responses](https://wiki.vg/RCON#Fragmentation).
        """
        _response: list[Packet] = []
        while self._reader:
            length_bytes = await self._reader.readexactly(4)
            length = struct.unpack("<i", length_bytes)[0]
            data = await self._reader.readexactly(length)
            packet = Packet(length_bytes + data)

            if _response:
                if packet.request_id == _response[0].request_id:
                    _response.append(packet)
                    if len(packet) < MAX_PACKET_SIZE_IN:
                        if packet.request_id in self._waiting:
                            self._waiting[packet.request_id].set_result(_response)
                        _response = []
                    continue
                else:
                    if _response[0].request_id in self._waiting:
                        self._waiting[_response[0].request_id].set_result(_response)
                    _response = []

            if len(packet) == MAX_PACKET_SIZE_IN:
                # maybe fragmented
                _response.append(packet)
                if self._writing_queue.empty():
                    await self._writing_queue.put(
                        Packet.from_payload("", PacketType.INVALID)
                    )
                continue

            if packet.request_id in self._waiting:
                self._waiting[packet.request_id].set_result([packet])

    async def __producer(self):
        """Sends queued packets to the server."""
        while self._writer:
            packet = await self._writing_queue.get()
            self._writer.write(packet)
            await self._writer.drain()

    async def _send(
        self, packet: Packet, *, timeout: Union[float, None] = 2
    ) -> list[Packet]:
        """Schedule a packet to be sent to the server, wait for the response and return it.

        :param packet: The packet to send.
        :type packet: Packet
        :param timeout: The time in seconds to wait for a response, defaults to `2`
        :type timeout: float | None, optional

        :raises asyncio.TimeoutError: If the response takes longer than `timeout`.

        :return: The response from the server.
        :rtype: list[Packet]
        """
        future = asyncio.get_running_loop().create_future()
        self._waiting[packet.request_id] = future
        await self._writing_queue.put(packet)
        try:
            return await asyncio.wait_for(future, timeout)
        except asyncio.TimeoutError:
            raise
        finally:
            self._waiting.pop(packet.request_id)

    async def close(self):
        """Closes the connection to the server and cancels all tasks."""
        if self.ready and self._writer and self._reader:
            self.__producer_task.cancel()
            self._writer.close()
            await self._writer.wait_closed()
            self.__consumer_task.cancel()
            self._writer = None
            self._reader = None
            self._ready = False

    async def __aenter__(self) -> Client:
        await self.connect()
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()
