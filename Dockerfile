FROM ghcr.io/astral-sh/uv:0.5-python3.13-alpine

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/usr/src/app/.venv/bin:$PATH"

WORKDIR /usr/src/app

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen \
    && adduser -D appuser \
    && chown -R appuser:appuser .

USER appuser

CMD ["python", "-m", "bot"]