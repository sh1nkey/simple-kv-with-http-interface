from collections.abc import Sequence
from typing_extensions import override
from src.dto import RequestData, ResponseData, StatusContainer
from src.kv_storage.interfaces import IReader, IStatus


class Reader(IReader):
    @override
    def __init__(self, read_dict: dict[str, str], status: IStatus) -> None:  # pyright: ignore
        self._read_dict = read_dict
        self._status = status

    @override
    def read(
        self, data: Sequence[RequestData]
    ) -> StatusContainer[Sequence[ResponseData]]:
        if len(data) == 1:
            val = self._read_dict.get(data[0].key, None)
            resp_data = ResponseData(value=val)
            return StatusContainer(
                data=(resp_data,),
                is_success=True,
                is_found=val is not None,
                is_single=True,
            )

        values: list[ResponseData] = []
        for arg in data:
            val = self._read_dict.get(arg.key, None)
            resp_data = ResponseData(value=val)
            _ = values.append(resp_data)

        return StatusContainer(
            data=values,
            is_found=True,
            is_success=True,
            is_single=False,
        )
