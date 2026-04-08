#!/usr/bin/env bash
# Production container start: Ollama (background) + FastAPI (foreground, PID 1 after exec).
set -euo pipefail

ollama serve &
OLLAMA_PID=$!

ready=0
for _ in $(seq 1 120); do
  if curl -sf "http://127.0.0.1:11434/api/tags" >/dev/null; then
    ready=1
    break
  fi
  sleep 1
done

if [[ "${ready}" -ne 1 ]]; then
  echo "error: Ollama did not respond at http://127.0.0.1:11434/api/tags within 120s" >&2
  exit 1
fi

if ! kill -0 "${OLLAMA_PID}" 2>/dev/null; then
  echo "error: ollama serve exited before FastAPI could start" >&2
  exit 1
fi

exec /opt/venv/bin/python /app/agent_main.py
