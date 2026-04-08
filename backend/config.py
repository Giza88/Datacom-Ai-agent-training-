import os

# Ollama (no API keys). The production Dockerfile sets OLLAMA_HOST to the in-container server.
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:latest")
