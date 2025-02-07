FROM python:3.12.3-slim-bookworm

COPY . /project

WORKDIR /project

RUN apt-get update && apt-get install -y libpq-dev gcc && \
pip install poetry && poetry install --no-root && \
pip install fastapi fastapi[standard] psycopg2


CMD ["fastapi", "run", "app/main.py"]