import aiohttp

from src.kv_storage.storage import KvStorage


async def test_many_success(run_serv: KvStorage) -> None:

    async with aiohttp.ClientSession() as session:
        key1 = "sigma1"
        val1 = "ligma1"

        key2 = "sigma2"
        val2 = "ligma2"

        async with session.post(f"http://localhost:8083/{key1}", json=val1) as response:
            assert response.status == 202
            text = await response.text()
            assert text == ""

        async with session.post(f"http://localhost:8083/{key2}", json=val2) as response:
            assert response.status == 202
            text = await response.text()
            assert text == ""

        async with session.get(f"http://localhost:8083/{key1},{key2}") as response:
            assert response.status == 200
            text = await response.text()
            assert text == "[ligma1,ligma2]"


async def test_many_one_not_found(run_serv: KvStorage) -> None:

    async with aiohttp.ClientSession() as session:
        key1 = "sigma3"
        val1 = "ligma3"

        key2 = "sigma4"

        async with session.post(f"http://localhost:8083/{key1}", json=val1) as response:
            assert response.status == 202
            text = await response.text()
            assert text == ""

        async with session.get(f"http://localhost:8083/{key1},{key2}") as response:
            assert response.status == 200
            text = await response.text()
            assert text == "[ligma3,None]"


async def test_many_all_not_found(run_serv: KvStorage) -> None:

    async with aiohttp.ClientSession() as session:
        key1 = "sigma5"
        key2 = "sigma6"

        async with session.get(f"http://localhost:8083/{key1},{key2}") as response:
            assert response.status == 200
            text = await response.text()
            assert text == "[None,None]"


# async def test_json(run_serv: KvStorage) -> None:
#     async with aiohttp.ClientSession() as session:
#         key = "ligma2"
#         val = {"ligma2": "ligma3"}

#         async with session.post(f"http://localhost:8083/{key}", json=val) as response:
#             assert response.status == 202
#             text = await response.text()
#             assert text == ""

#         async with session.get(f"http://localhost:8083/{key}") as response:
#             assert response.status == 200
#             resp_data = await response.text()
#             assert resp_data == json.dumps(val)


# async def test_unknown_method(run_serv: KvStorage) -> None:
#     async with aiohttp.ClientSession() as session:
#         val = {"ligma2": "ligma3"}

#         async with session.patch("http://localhost:8083", json=val) as response:
#             assert response.status == 404
#             text = await response.text()
#             assert text == ""
