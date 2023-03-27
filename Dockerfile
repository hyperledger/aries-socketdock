FROM python:3.9

ENV POETRY_VERSION=1.3.2

WORKDIR /code

RUN pip install "poetry==$POETRY_VERSION"
COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY server .

CMD [ "python", "./socketdock.py" ]
