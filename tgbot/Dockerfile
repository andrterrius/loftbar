FROM ghcr.io/astral-sh/uv:python3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app/

RUN uv sync
ENV PATH="/app/.venv/bin:${PATH}"

CMD ["uv", "run", "python", "-m", "app.entrypoints.__main__"]