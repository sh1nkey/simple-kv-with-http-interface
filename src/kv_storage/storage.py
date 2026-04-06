from collections.abc import Sequence
from typing import Any, Self
from src.dto import RequestData, ResponseData, StatusContainer
from src.kv_storage.interfaces import IReader, IWriter


class Status:
    def __init__(self) -> None:
        self._is_active = True

    def is_active(self) -> bool:
        return self._is_active

    def set_inactive(self) -> None:
        self._is_active = False


class KvStorage:
    def __init__(
        self, reader: type[IReader], writer: type[IWriter], file_name: str = "data.txt"
    ) -> None:
        self._file = open(file_name, "a+")

        self._read_dict = dict[str, str]()

        self._status = Status()

        self._writer = writer(self._file, self._read_dict, self._status)
        self._reader = reader(self._read_dict, self._status)

    async def write(self, data: RequestData) -> bool:
        return await self._writer.write(data)

    async def read(
        self, data: Sequence[RequestData]
    ) -> StatusContainer[Sequence[ResponseData]]:
        try:
            return self._reader.read(data)
        except Exception:
            return StatusContainer(
                data=(ResponseData(value=None),),
                is_success=False,
                is_found=False,
            )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self, type: type[Exception], value: Exception, traceback: Any
    ) -> None:
        try:
            ...
        finally:
            self._status.set_inactive()
            await self._writer.stop()
