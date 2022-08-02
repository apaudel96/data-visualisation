FROM python:3.10-slim
WORKDIR /app
RUN pip install pdm
COPY pyproject.toml .
COPY pdm.lock .
RUN pdm install
COPY . .
CMD [ "pdm", "run", "panel", "serve", "sales.py", "simple_sales.py", "--port", "${PORT}" ]
