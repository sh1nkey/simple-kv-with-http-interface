# syntax=docker/dockerfile:1.9
FROM python:3.13-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app


ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_NO_DEV=1

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


FROM python:3.13-slim-bookworm


WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src ./src

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

CMD ["python", "-m", "src.main"]
