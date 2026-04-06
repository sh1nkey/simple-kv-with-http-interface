from collections.abc import Awaitable, Sequence
from typing import Callable, Protocol, runtime_checkable

from src.dto import RequestData, ResponseData, StatusContainer


RequestBytes = bytes  # response data in format of bytes
RequestStr = str  # request data in format of string
ResponseBytes = bytes  # response data in format of bytes


@runtime_checkable
class IRequestHandler(Protocol):
    """
    Maps bytes data to DTO, then returns bytes response
    depending on the success of func call
    """

    def __init__(self, func: Callable[[RequestData], Awaitable[bool]]) -> None: ...
    async def handle(self, request: RequestBytes, body: str) -> ResponseBytes: ...


@runtime_checkable
class IBodylessRequestHandler(Protocol):
    """
    Maps bytes data to DTO, then returns bytes response
    depending on the StatusContainer values

    (Used for requests without body, e.g. GET)
    """

    def __init__(
        self,
        func: Callable[
            [Sequence[RequestData]], Awaitable[StatusContainer[Sequence[ResponseData]]]
        ],
    ) -> None: ...

    async def handle_no_body(self, request: RequestBytes) -> ResponseBytes: ...


class IHandlerMapper(Protocol):
    def get_handler(
        self, request: RequestStr
    ) -> IRequestHandler | IBodylessRequestHandler | None: ...
