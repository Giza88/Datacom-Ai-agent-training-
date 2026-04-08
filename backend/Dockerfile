FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV OLLAMA_HOST=http://127.0.0.1:11434
ENV PATH="/opt/venv/bin:$PATH"

# Base tools, Python + venv, and native libs for python-pptx / Manim wheels
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

# Install Ollama (https://ollama.com/)
RUN curl -fsSL https://ollama.com/install.sh | sh

RUN mkdir -p /root/.ollama/models

# Pull model while a transient ollama serve is up (large layer)
RUN bash -c 'set -e; \
    ollama serve >/tmp/ollama-build.log 2>&1 & pid=$!; \
    for i in $(seq 1 120); do \
      curl -sf http://127.0.0.1:11434/api/tags >/dev/null && break; \
      sleep 1; \
    done; \
    ollama pull llama3.1:latest; \
    kill "$pid"; wait "$pid" 2>/dev/null || true'

WORKDIR /app

COPY requirements.txt .
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000
EXPOSE 11434

ENTRYPOINT ["/app/docker-entrypoint.sh"]
