import aiohttp

from src.kv_storage.storage import KvStorage


async def test_set_no_body(run_serv: KvStorage) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8083/key") as response:
            assert response.status == 500
            text = await response.text()
            assert text == ""


async def test_set_no_key(run_serv: KvStorage) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8083/") as response:
            assert response.status == 500
            text = await response.text()
            assert text == ""
