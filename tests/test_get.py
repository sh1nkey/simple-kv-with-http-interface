import json
import aiohttp

from src.kv_storage.storage import KvStorage


async def test_string(run_serv: KvStorage) -> None:

    async with aiohttp.ClientSession() as session:
        key = "ligma1"
        val = "ligma2"

        async with session.post(f"http://localhost:8083/{key}", json=val) as response:
            assert response.status == 202
            text = await response.text()
            assert text == ""

        async with session.get(f"http://localhost:8083/{key}") as response:
            assert response.status == 200
            text = await response.text()
            assert text == val


async def test_json(run_serv: KvStorage) -> None:
    async with aiohttp.ClientSession() as session:
        key = "ligma2"
        val = {"ligma2": "ligma3"}

        async with session.post(f"http://localhost:8083/{key}", json=val) as response:
            assert response.status == 202
            text = await response.text()
            assert text == ""

        async with session.get(f"http://localhost:8083/{key}") as response:
            assert response.status == 200
            resp_data = await response.text()
            assert resp_data == json.dumps(val)


async def test_unknown_method(run_serv: KvStorage) -> None:
    async with aiohttp.ClientSession() as session:
        val = {"ligma2": "ligma3"}

        async with session.patch("http://localhost:8083", json=val) as response:
            assert response.status == 404
            text = await response.text()
            assert text == ""
