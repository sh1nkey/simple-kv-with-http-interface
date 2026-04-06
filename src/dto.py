from dataclasses import dataclass


@dataclass(frozen=True)
class RequestData:
    key: str
    value: str | None = None


@dataclass(frozen=True)
class ResponseData:
    value: str | None = None


@dataclass(frozen=True)
class StatusContainer[T]:
    data: T

    is_success: bool = True
    is_found: bool = True
    is_single: bool = False
