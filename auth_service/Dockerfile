FROM python:3.13-alpine

RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /app
COPY . /app

RUN uv pip install -r <(uv pip compile pyproject.toml --generate-hashes)
RUN uv pip install -e .
EXPOSE 8000

CMD ["uv", "run", "uvicorn", "your_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
