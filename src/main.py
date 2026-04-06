import asyncio
from src.kv_storage.reader import Reader
from src.kv_storage.storage import KvStorage
from src.kv_storage.writer import Writer
from src.handlers.handler import ReadHandler, SetHandler
from src.handlers.handler_mapper import HandlerMapper, HTTPMethodEnum
from src.server.server import ServerConfig
from src.server.server import run_server
import logging

logging.basicConfig(level=logging.INFO)


async def main():
    config = ServerConfig(port=8083)

    async with KvStorage(Reader, Writer, "test_data.txt") as kv_db:
        logging.info("KvStorage initialized")

        handler_mapper = HandlerMapper(
            (
                (HTTPMethodEnum.GET, ReadHandler(kv_db.read)),
                (HTTPMethodEnum.POST, SetHandler(kv_db.write)),
            )
        )

        await run_server(config, handler_mapper)


if __name__ == "__main__":
    try:
        import uvloop  # pyright: ignore[reportMissingImports]

        uvloop.install()  # pyright: ignore[reportUnknownMemberType]
    except ModuleNotFoundError:
        logging.warning("uvloop is not installed, falling back to default event loop")

    asyncio.run(main())
