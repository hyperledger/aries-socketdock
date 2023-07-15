FROM python:3.9-slim-bullseye
WORKDIR /usr/src/app

ENV POETRY_VERSION=1.4.2

RUN apt-get update && apt-get install -y curl && apt-get clean
RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml README.md ./
RUN mkdir -p socketdock && touch socketdock/__init__.py
RUN poetry config virtualenvs.create false \
  && poetry install --without=dev --no-interaction --no-ansi

COPY socketdock socketdock

ENTRYPOINT ["python",  "-m", "socketdock" ]
