FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.18 /uv /uvx /bin/

# ./backend を /app にマウントすると /app/.venv が Mac 側の .venv で隠れるため、
# コンテナの仮想環境はマウント先の外に作る。
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-install-project --no-cache
