"""Ollama HTTP helpers and JSON parsing for slide agents."""
import json
from typing import Any

import aiohttp

from config import OLLAMA_HOST, OLLAMA_MODEL


def ollama_base_url() -> str:
    return OLLAMA_HOST.rstrip("/")


def extract_json_payload(raw_text: str) -> dict[str, Any]:
    text = (raw_text or "").strip()
    if not text:
        raise ValueError("Empty response text")
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start : end + 1]
    return json.loads(text)


async def ollama_generate(session: aiohttp.ClientSession, prompt: str) -> str:
    url = f"{ollama_base_url()}/api/generate"
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    async with session.post(url, json=payload) as resp:
        resp.raise_for_status()
        data = await resp.json()
        return (data.get("response") or "").strip()
