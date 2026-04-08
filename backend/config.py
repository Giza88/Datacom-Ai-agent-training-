import os

# Ollama (no API keys). Override via environment when needed (e.g. Docker → host Ollama).
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:latest")
