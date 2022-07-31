
FROM python:3.10-slim
# RUN adduser --disabled-password app
# USER app
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
