from asyncio.queues import Queue


import asyncio
from io import TextIOWrapper
from typing import Never
from typing_extensions import override
from src.dto import RequestData
from src.kv_storage.interfaces import IStatus, IWriter


class Writer(IWriter):
    @override
    def __init__(  # pyright: ignore
        self, file: TextIOWrapper, read_dict: dict[str, str], status: IStatus
    ) -> None:
        self._read_dict = read_dict
        self._file = file

        self._load_from_file()
        self._clean_from_duplicates()

        self._queue: Queue[RequestData] = asyncio.Queue(500_000)
        self._status = status

        self.__worker = asyncio.create_task(self._run_worker())

    @override
    async def write(self, data: RequestData) -> bool:
        if self._status.is_active():
            await self._queue.put(data)
            return True

        return False

    async def _run_worker(self) -> Never:
        while True:
            task = await self._queue.get()
            self._write_to_file(task)
            self._queue.task_done()

    def _write_to_file(self, data: RequestData) -> None:
        val_to_write = data.value or ""
        self._read_dict[data.key] = val_to_write
        _ = self._file.write(data.key + " " + val_to_write + "\n")
        self._file.flush()

    def _load_from_file(self) -> None:
        if not self._file:
            raise RuntimeError("no file exists")

        self._file.seek(0)

        for line in self._file:
            line = line.strip()

            parts = line.split(" ", 1)
            if len(parts) == 2:
                key, value = parts
                self._read_dict[key] = value
            elif len(parts) == 1:
                self._read_dict[parts[0]] = ""

        _ = self._file.seek(0, 2)

    def _clean_from_duplicates(self) -> None:
        if not self._file:
            raise RuntimeError("no file exists")

        self._file.seek(0)
        self._file.truncate(0)

        for key, value in self._read_dict.items():
            if value:
                line = f"{key} {value}\n"
            else:
                line = f"{key}\n"
            self._file.write(line)
        self._file.seek(0, 2)

    @override
    async def stop(self):
        await self._queue.join()
        self.__worker.cancel()
        self._file.close()
