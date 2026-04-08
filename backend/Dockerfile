FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV OLLAMA_HOST=http://127.0.0.1:11434

# System deps: Python, venv, curl, Cairo/Pango (Manim / rendering), build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    && rm -rf /var/lib/apt/lists/*

# Ollama CLI
RUN curl -fsSL https://ollama.com/install.sh | sh

RUN mkdir -p /root/.ollama/models

# Bake model: start Ollama briefly, wait for API, pull, then stop (large image layer)
RUN bash -c 'set -e; \
    ollama serve >/tmp/ollama-build.log 2>&1 & pid=$!; \
    for i in $(seq 1 120); do \
      curl -sf http://127.0.0.1:11434/api/tags >/dev/null && break; \
      sleep 1; \
    done; \
    curl -sf http://127.0.0.1:11434/api/tags >/dev/null || { echo "Ollama did not start:"; cat /tmp/ollama-build.log; exit 1; }; \
    ollama pull llama3.1:latest; \
    kill "$pid"; wait "$pid" 2>/dev/null || true'

# Python virtualenv on PATH for runtime and entrypoint
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000
EXPOSE 11434

# Azure / Container Apps: allow cold start for Ollama + model load
HEALTHCHECK --interval=30s --timeout=10s --start-period=300s --retries=3 \
    CMD curl -sf http://127.0.0.1:8000/health >/dev/null || exit 1

CMD ["/app/docker-entrypoint.sh"]
