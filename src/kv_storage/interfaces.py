from _io import TextIOWrapper
from collections.abc import Sequence
from typing import Protocol

from src.dto import RequestData, ResponseData, StatusContainer


class IStatus(Protocol):
    """
    Simple class to track bool state and change it
    """

    def is_active(self) -> bool: ...

    def set_inactive(self) -> None: ...


class IWriter(Protocol):
    def __init__(
        self, file: TextIOWrapper, read_dict: dict[str, str], status: IStatus
    ) -> None: ...

    async def write(self, data: RequestData) -> bool: ...

    async def stop(self) -> None: ...


class IReader(Protocol):
    def __init__(self, read_dict: dict[str, str], status: IStatus) -> None: ...

    def read(
        self, data: Sequence[RequestData]
    ) -> StatusContainer[Sequence[ResponseData]]: ...
