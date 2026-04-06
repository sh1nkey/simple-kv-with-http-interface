from collections.abc import AsyncGenerator
import logging
from typing import Any


import asyncio


from src.kv_storage.reader import Reader
from src.kv_storage.storage import KvStorage
from src.kv_storage.writer import Writer
from src.server.server import run_server, ServerConfig
from src.handlers.handler_mapper import HandlerMapper, HTTPMethodEnum
from src.handlers.handler import ReadHandler, SetHandler
import pytest


try:
    import uvloop  # pyright: ignore[reportMissingImports]

    uvloop.install()
except ModuleNotFoundError:
    logging.warning("uvloop is not installed, falling back to default event loop")


@pytest.fixture()
async def run_serv() -> AsyncGenerator[KvStorage, Any]:
    logging.basicConfig(level=logging.DEBUG)

    async with KvStorage(Reader, Writer, "test_data.txt") as kv_db:
        config = ServerConfig(port=8083)

        handler_mapper = HandlerMapper(
            (
                (HTTPMethodEnum.GET, ReadHandler(kv_db.read)),
                (HTTPMethodEnum.POST, SetHandler(kv_db.write)),
            )
        )

        task = asyncio.create_task(run_server(config, handler_mapper))

        yield kv_db

    task.cancel()
