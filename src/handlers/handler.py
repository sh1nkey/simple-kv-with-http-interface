from collections.abc import Awaitable, Callable, Sequence
from typing_extensions import override
from src.dto import RequestData, ResponseData, StatusContainer
from src.interfaces import (
    IBodylessRequestHandler,
    IRequestHandler,
    RequestBytes,
    ResponseBytes,
)
from src.handlers import resp_constants


class ReadHandler(IBodylessRequestHandler):
    @override
    def __init__(  # pyright: ignore[reportMissingSuperCall]
        self,
        func: Callable[
            [Sequence[RequestData]], Awaitable[StatusContainer[Sequence[ResponseData]]]
        ],
    ) -> None:
        self._func = func

    @override
    async def handle_no_body(self, request: bytes) -> ResponseBytes:
        request_data = self._parse_request(request)
        resp_data = await self._func(request_data)
        return self._build_response(resp_data)

    @staticmethod
    def _parse_request(request: bytes) -> Sequence[RequestData]:
        request_str = request.decode()
        lines = request_str.splitlines()
        _, path, _ = lines[0].split()

        keys = path.split("/")[-1]

        key_list = keys.split(",")
        if len(key_list) == 1:
            return (RequestData(key=key_list[0], value=None),)

        return [RequestData(key=key, value=None) for key in key_list]

    @staticmethod
    def _build_response(resp: StatusContainer[Sequence[ResponseData]]) -> ResponseBytes:
        if resp.is_success is False:
            return resp_constants.RESPONSE_ERR

        if resp.is_found is False:
            return resp_constants.RESPONSE_NOT_FOUND

        if resp.is_single:
            val = resp.data[0].value or ""
            resp_length = len(val)
            encoded_val = val.encode()
            response = (
                resp_constants.RESPONSE_GET_SUCCESS.format(resp_length)
            ).encode() + encoded_val
            return response

        val_list = [val.value for val in resp.data]
        val_list_str = "["
        for idx, val in enumerate(val_list):
            val_list_str += str(val)
            if idx != len(val_list) - 1:
                val_list_str += ","

        val_list_str += "]"
        encoded_val = val_list_str.encode()
        response = (
            resp_constants.RESPONSE_GET_SUCCESS.format(len(val_list_str))
        ).encode() + encoded_val
        return response


class SetHandler(IRequestHandler):
    @override
    def __init__(self, func: Callable[[RequestData], Awaitable[bool]]):  # pyright: ignore[reportMissingSuperCall]
        self.func = func

    @override
    async def handle(self, request: RequestBytes, body: str) -> ResponseBytes:
        request_data = self._parse_request(request, body)
        if request_data is None:
            return resp_constants.RESPONSE_ERR

        resp_data = await self.func(request_data)
        return self._build_response(resp_data)

    @staticmethod
    def _parse_request(request: RequestBytes, body: str) -> RequestData | None:
        request_str = request.decode()
        lines = request_str.splitlines()
        _, path, _ = lines[0].split()
        key = path.lstrip("/")
        if len(key) == 0:
            return None
        return RequestData(key=key, value=body)

    @staticmethod
    def _build_response(result: bool) -> ResponseBytes:
        return (
            resp_constants.RESPONSE_SET_SUCCESS
            if result
            else resp_constants.RESPONSE_ERR
        )
