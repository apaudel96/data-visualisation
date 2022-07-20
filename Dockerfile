FROM python:3.10-slim

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .
RUN pip install poetry
RUN poetry install

COPY . .
