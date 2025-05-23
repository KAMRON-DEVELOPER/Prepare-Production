FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /pod

COPY main.py ./
COPY ./pyproject.toml ./
COPY ./uv.lock ./
COPY ./app ./app
COPY ./favicon.ico ./

RUN uv sync --locked

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]