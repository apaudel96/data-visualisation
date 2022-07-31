# FROM python:3.10-slim

# WORKDIR /app

# COPY poetry.lock .
# COPY pyproject.toml .
# RUN pip install poetry
# RUN poetry install

# COPY . .
FROM python:3.10-slim as builder
WORKDIR /build
COPY requirements.txt .
# RUN python -m venv venv
RUN pip install --user -r requirements.txt


FROM python:3.10-alpine
RUN adduser --disabled-password app
USER app
WORKDIR /app
COPY --from=builder $HOME/.local $HOME/.local
RUN export PATH=$PATH:$HOME/.local/bin
COPY . .
