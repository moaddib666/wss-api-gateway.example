FROM python:3-alpine

WORKDIR /home/application
COPY worker.py client.py poetry.lock pyproject.toml /home/application/
RUN pip install -U poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi
