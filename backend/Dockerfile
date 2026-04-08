# Production backend: Ubuntu 22.04 + Ollama + FastAPI (single container).
# Ollama runs beside the API at runtime; the default model is pulled during `docker build`.
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV OLLAMA_HOST=http://127.0.0.1:11434
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    git \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    pkg-config \
    libcairo2-dev \
    libpango1.0-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.com/install.sh | sh

RUN mkdir -p /root/.ollama/models

# Pre-pull model (large layer); fail the build if Ollama never becomes ready or pull fails
RUN bash -c 'set -e; \
    ollama serve >/tmp/ollama-build.log 2>&1 & pid=$!; \
    for i in $(seq 1 120); do \
      curl -sf http://127.0.0.1:11434/api/tags >/dev/null && break; \
      sleep 1; \
    done; \
    curl -sf http://127.0.0.1:11434/api/tags >/dev/null || { echo "Ollama did not start:"; cat /tmp/ollama-build.log; exit 1; }; \
    ollama pull llama3.1:latest; \
    kill "$pid"; wait "$pid" 2>/dev/null || true'

WORKDIR /app

COPY requirements.txt .
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000 11434

# Allow time for Ollama + model on cold start (e.g. Azure Container Apps).
HEALTHCHECK --interval=30s --timeout=5s --start-period=300s --retries=3 \
    CMD curl -sf http://127.0.0.1:8000/health >/dev/null || exit 1

# Runtime: docker-entrypoint.sh starts Ollama, waits for /api/tags, then execs FastAPI (see script).
CMD ["/app/docker-entrypoint.sh"]
