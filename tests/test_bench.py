import asyncio
import logging
import time

# import cProfile
# import pstats
import pytest
import aiohttp

from src.kv_storage.storage import KvStorage


logging.basicConfig(level=logging.DEBUG)


@pytest.mark.slow
async def test_sync_bench(run_serv: KvStorage) -> None:
    async with aiohttp.ClientSession() as session:
        val = {"ligma3": "ligma4"}

        time_start = time.time()

        for i in range(5000):
            async with session.patch(f"http://localhost:8083/{i}", json=val) as _:
                ...

        time_failed = time.time()
        logging.debug(
            f"\n(NONCONCURRENT) Time taking for server to give 5000 404 responses: {time_failed - time_start} seconds\n"
        )

        for i in range(5000):
            async with session.post(f"http://localhost:8083/{i}", json=val) as _:
                ...

        await run_serv._writer._queue.join()
        time_end = time.time()
        logging.debug(
            f"(NONCONCURRENT)Time taken for 5000: {time_end - time_failed} seconds\n"
        )


@pytest.mark.slow
async def test_async_bench(run_serv: KvStorage) -> None:
    val = {"ligma3": "ligma4"}

    connector = aiohttp.TCPConnector(limit=20)

    async with aiohttp.ClientSession(connector=connector) as session:
        time_start = time.time()

        tasks = []
        for i in range(5000):
            tasks.append(
                asyncio.create_task(
                    make_patch_request(session, f"http://localhost:8083/{i}")
                )
            )

        _ = await asyncio.gather(*tasks, return_exceptions=True)

        time_after_patch = time.time()
        logging.debug(
            f"\n(CONCURRENT)PATCH 5000 requests took: {time_after_patch - time_start:.3f} seconds"
        )

        tasks = []
        for i in range(5000):
            tasks.append(
                asyncio.create_task(
                    make_post_request(session, f"http://localhost:8083/{i}", val)
                )
            )

        _ = await asyncio.gather(*tasks, return_exceptions=True)

        time_end_post = time.time()
        logging.debug(
            f"\n(CONCURRENT)POST 5000 requests took: {time_end_post - time_after_patch:.3f} seconds"
        )

        if hasattr(run_serv, "_writer") and hasattr(run_serv._writer, "_queue"):
            await run_serv._writer._queue.join()  # лучше await, если это asyncio.Queue

        tasks = []
        for i in range(5000):
            tasks.append(
                asyncio.create_task(
                    make_get_request(session, f"http://localhost:8083/{i}")
                )
            )

        # profiler = cProfile.Profile()
        # profiler.enable()
        _ = await asyncio.gather(*tasks, return_exceptions=True)
        # profiler.disable()

        time_end_get = time.time()
        logging.debug(
            f"\n(CONCURRENT)GET 5000 requests took: {time_end_get - time_end_post:.3f} seconds\n"
        )

        # Анализ профилирования для GET
        # stats = pstats.Stats(profiler).sort_stats("cumtime")
        # logging.debug("Top functions in GET requests:")
        # stats.logging.debug_stats(10)


async def make_post_request(session: aiohttp.ClientSession, url: str, json_data: dict):
    try:
        async with session.post(url, json=json_data) as resp:
            return resp.status
    except Exception as e:
        logging.debug(f"Post error {url}: {e}")
        return None


async def make_patch_request(session: aiohttp.ClientSession, url: str):
    try:
        async with session.patch(url) as resp:
            return resp.status
    except Exception as e:
        logging.debug(f"Patch error {url}: {e}")
        return None


async def make_get_request(session: aiohttp.ClientSession, url: str):
    try:
        async with session.get(url) as resp:
            _ = await resp.text()
            return resp.status
    except Exception as e:
        logging.debug(f"Get error {url}: {e}")
        return None
