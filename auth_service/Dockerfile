FROM python:3.13-alpine

RUN apk update && apk add --no-cache curl
RUN apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    cp /root/.local/bin/uv /usr/local/bin/


WORKDIR /app
COPY . /app
RUN uv pip compile pyproject.toml --generate-hashes > requirements.txt
RUN uv venv && uv python install 3.13
RUN uv pip install -r requirements.txt
RUN uv pip install -e .
EXPOSE 8000