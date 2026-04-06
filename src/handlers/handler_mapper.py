from collections.abc import Sequence
from enum import StrEnum
from typing_extensions import override
from src.interfaces import (
    IBodylessRequestHandler,
    IRequestHandler,
    IHandlerMapper,
    RequestStr,
)


class HTTPMethodEnum(StrEnum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"


class HandlerMapper(IHandlerMapper):
    def __init__(
        self,
        handlers: Sequence[
            tuple[HTTPMethodEnum, IRequestHandler | IBodylessRequestHandler]
        ],
    ):
        self.map_route_handlers: dict[
            HTTPMethodEnum, IRequestHandler | IBodylessRequestHandler
        ] = dict()
        for method, handler in handlers:
            self.map_route_handlers[method] = handler

    @override
    def get_handler(
        self, request: RequestStr
    ) -> IRequestHandler | IBodylessRequestHandler | None:
        splitted = request.split()
        if len(splitted) == 0:
            return None

        method = splitted[0]

        handler = self.map_route_handlers.get(HTTPMethodEnum(method), None)
        return handler
