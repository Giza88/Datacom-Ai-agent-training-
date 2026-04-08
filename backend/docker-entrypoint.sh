#!/usr/bin/env bash
set -euo pipefail

ollama serve &
OLLAMA_PID=$!

for _ in $(seq 1 90); do
  if curl -sf "http://127.0.0.1:11434/api/tags" >/dev/null; then
    break
  fi
  sleep 1
done

if ! kill -0 "${OLLAMA_PID}" 2>/dev/null; then
  echo "ollama serve failed to stay running" >&2
  exit 1
fi

exec /opt/venv/bin/python /app/agent_main.py
