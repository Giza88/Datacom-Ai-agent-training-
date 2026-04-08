"""Async HTTP client for the local Ollama API (`/api/generate`)."""

from __future__ import annotations

import aiohttp

from config import OLLAMA_HOST, OLLAMA_MODEL


class OllamaClient:
    """POST JSON to Ollama and return the ``response`` text (non-streaming)."""

    def __init__(
        self,
        base_url: str | None = None,
        default_model: str | None = None,
    ) -> None:
        self.base_url = (base_url or OLLAMA_HOST).rstrip("/")
        self.default_model = default_model or OLLAMA_MODEL

    def generate_url(self) -> str:
        return f"{self.base_url}/api/generate"

    async def generate(
        self,
        session: aiohttp.ClientSession,
        prompt: str,
        *,
        model: str | None = None,
    ) -> str:
        payload = {
            "model": model or self.default_model,
            "prompt": prompt,
            "stream": False,
        }
        async with session.post(self.generate_url(), json=payload) as resp:
            resp.raise_for_status()
            data = await resp.json()
            return (data.get("response") or "").strip()
