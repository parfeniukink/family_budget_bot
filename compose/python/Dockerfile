FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

COPY poetry.lock pyproject.toml ./

RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # cleaning up unused files
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install

COPY ./ ./
