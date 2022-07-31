# FROM python:3.10-slim

# WORKDIR /app

# COPY poetry.lock .
# COPY pyproject.toml .
# RUN pip install poetry
# RUN poetry install

# COPY . .
FROM python:3.10-slim as builder
WORKDIR /build
RUN python -m venv venv
COPY requirements.txt .
RUN venv/bin/pip install -r requirements.txt


FROM python:3.10-alpine
RUN adduser --disabled-password app
USER app
WORKDIR /app
COPY --from=builder /build/venv ./venv
COPY . .
