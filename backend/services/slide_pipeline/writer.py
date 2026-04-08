import json
import logging

import aiohttp

from services.llm_utils import extract_json_payload
from services.ollama_client import OllamaClient

logger = logging.getLogger(__name__)

WRITER_INSTRUCTIONS = """You are a slide content writer. Given a title and focus, return ONLY valid JSON:
{"title": "...", "bullets": ["...", "...", "...", "..."]}

Bullets: concise, punchy, audience-appropriate.
JSON only."""


class WriterAgent:
    def __init__(self, client: OllamaClient | None = None) -> None:
        self._ollama = client if client is not None else OllamaClient()

    async def run(self, session: aiohttp.ClientSession, item: dict) -> dict:
        payload_text = f"{WRITER_INSTRUCTIONS}\n\n{json.dumps(item)}"
        try:
            raw = await self._ollama.generate(session, payload_text)
            if not raw.strip():
                raise RuntimeError("Writer returned an empty response")

            parsed = extract_json_payload(raw)
            title = parsed.get("title")
            bullets = parsed.get("bullets")
            if not isinstance(title, str) or not title.strip():
                raise RuntimeError("Writer JSON missing 'title'")
            if not isinstance(bullets, list):
                raise RuntimeError("Writer JSON missing 'bullets' list")

            clean_bullets = [str(b).strip() for b in bullets if str(b).strip()]
            if not clean_bullets:
                clean_bullets = [
                    str(item.get("focus") or item.get("title") or "Key point")
                ]

            return {"title": title.strip(), "bullets": clean_bullets}
        except Exception as e:
            logger.warning(
                "Writer failed for slide %r: %s", item.get("title"), e
            )
            return {
                "title": item.get("title") or "Untitled",
                "bullets": ["Content generation failed"],
            }
