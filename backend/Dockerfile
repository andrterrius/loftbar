FROM ghcr.io/astral-sh/uv:python3.13-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY .. /app/

RUN uv sync
ENV PATH="/app/.venv/bin:${PATH}"

EXPOSE ${BACKEND_PORT}

CMD ["alembic", "upgrade", "head"]
CMD ["uvicorn", "entrypoints.__main__:app", "--host", "0.0.0.0", "--port", "${BACKEND_PORT}"]