# --- Stage 1: Build dependencies ---
FROM python:3.11-slim AS builder

WORKDIR /app

ARG POETRY_VERSION=2.1.0
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock* ./
COPY alembic.ini alembic/ ./

RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi --without dev

COPY . .

# --- Stage 2: Runtime image ---
FROM python:3.11-slim AS runtime

WORKDIR /app

RUN addgroup --system app && adduser --system --group app

COPY --from=builder /usr/local/lib/python3.11/site-packages \
                     /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/poetry /usr/local/bin/poetry

COPY --from=builder /app/app ./app
COPY --from=builder /app/alembic.ini ./
COPY --from=builder /app/alembic ./alembic

USER app

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
