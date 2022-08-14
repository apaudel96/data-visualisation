FROM python:3.10-slim
WORKDIR /app
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy --ignore-pipfile
COPY . .
CMD panel serve sales.py simple_sales.py --port $PORT
