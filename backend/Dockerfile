FROM ghcr.io/astral-sh/uv:python3.13-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app/

RUN uv sync
ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE ${BACKEND_PORT}

CMD sh -c "alembic upgrade head && uvicorn app.entrypoints.__main__:app --host 0.0.0.0 --port ${BACKEND_PORT} --forwarded-allow-ips='*' --proxy-headers"