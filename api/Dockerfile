FROM ubuntu:latest AS base

# Install Python 3.12, curl and security updates
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3.12 python3-pip curl ca-certificates ffmpeg && \
    curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /api

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev

COPY app/ app/

EXPOSE 80

CMD ["uv", "run", "fastapi", "run", "--port", "80", "--host", "0.0.0.0"]