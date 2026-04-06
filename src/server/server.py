from collections.abc import Awaitable
from dataclasses import dataclass
import asyncio
import logging
from typing import Callable
from src.interfaces import (
    IBodylessRequestHandler,
    IRequestHandler,
    IHandlerMapper,
)
from src.server import resp_constants


@dataclass(frozen=True)
class ServerConfig:
    port: int = 8083


async def run_server(config: ServerConfig, handler_mapper: IHandlerMapper):
    server = Server(config, handler_mapper)

    async def handle_client(
        reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        headers, body = await server.parse_reader(reader)

        handler = server.handler_mapper.get_handler(headers.decode())

        response: bytes = b""
        if handler is None:
            response = resp_constants.RESPONSE_NOT_FOUND
        elif body and isinstance(handler, IRequestHandler):
            response = await handler.handle(headers, body)
        elif not body and isinstance(handler, IBodylessRequestHandler):
            response = await handler.handle_no_body(headers)
        else:
            response = resp_constants.RESPONSE_ERR

        writer.write(response)
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    await server.run(handle_client)


class Server:
    def __init__(self, config: ServerConfig, handler_mapper: IHandlerMapper) -> None:
        self.config = config
        self.handler_mapper = handler_mapper

    async def run(
        self,
        handle_client: Callable[
            [asyncio.StreamReader, asyncio.StreamWriter], Awaitable[None]
        ],
    ) -> None:
        server = await asyncio.start_server(handle_client, "0.0.0.0", self.config.port)
        async with server:
            logging.info(f"Starting server on port {self.config.port}")
            await server.serve_forever()

    @staticmethod
    async def parse_reader(reader: asyncio.StreamReader) -> tuple[bytes, str | None]:

        try:
            headers_bytes = await reader.readuntil(b"\r\n\r\n")
        except asyncio.IncompleteReadError:
            # logging.warning("Received incomplete request, closing connection")
            return b"", None

        headers_str = headers_bytes.decode()
        content_length = 0

        for line in headers_str.split("\r\n"):
            if line.lower().startswith("content-length:"):
                try:
                    content_length = int(line.split(":", 1)[1].strip())
                except ValueError:
                    pass

        body = b""
        if content_length > 0 and headers_str.split()[0] != "GET":
            body = await reader.readexactly(content_length)
            if body.startswith(b'"') and body.endswith(b'"'):
                body = body[1:-1]

        return headers_bytes, body.decode() if body else None
