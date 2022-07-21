
FROM python:3.8 as dev

ENV _ENV=development \
    POETRY_VERSION=1.1.13

WORKDIR /app
COPY . /app 


RUN pip3 install "poetry==$POETRY_VERSION"

RUN poetry config virtualenvs.create false
RUN poetry install $(test "$_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

EXPOSE 8000


FROM python:3.8 as prod

ENV _ENV=development \
    POETRY_VERSION=1.1.13

WORKDIR /app
COPY --from=dev /app/src /app 

RUN pip3 install "poetry==$POETRY_VERSION"

COPY pyproject.toml /app 
COPY poetry.lock /app 

RUN poetry config virtualenvs.create false
RUN poetry install $(test "$_ENV" == production && echo "--no-dev") --no-interaction --no-ansi

EXPOSE 8000

