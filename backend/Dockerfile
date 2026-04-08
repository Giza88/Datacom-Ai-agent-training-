FROM ubuntu:22.04

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV OLLAMA_HOST=http://127.0.0.1:11434

# Install system dependencies
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

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama temporarily to pull the model
RUN ollama serve & \
    pid=$! && \
    sleep 5 && \
    curl --retry 20 --retry-delay 3 --retry-connrefused http://127.0.0.1:11434/api/tags && \
    ollama pull llama3.1:latest && \
    kill $pid

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy app
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Healthcheck for Azure
HEALTHCHECK --interval=30s --timeout=10s --start-period=300s \
  CMD curl -f http://127.0.0.1:8000/health || exit 1

# Copy entrypoint
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000
EXPOSE 11434

CMD ["/app/docker-entrypoint.sh"]
