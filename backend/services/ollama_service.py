"""Slide outline generation via local Ollama (Microsoft Agent Framework)."""
import json

from agent_framework.ollama import OllamaChatClient

from config import OLLAMA_HOST, OLLAMA_MODEL

SYSTEM_PROMPT = """You are a professional presentation writer.
Given a topic and slide count, return ONLY valid JSON - no markdown:
{"slides": [{"title": "...", "bullets": ["...", "...", "..."]}]}"""

_client: OllamaChatClient | None = None


def _get_client() -> OllamaChatClient:
    """Single Ollama chat client (maps to the user's Ollama HTTP server)."""
    global _client
    if _client is None:
        # host = base URL for Ollama (default http://localhost:11434); model = pulled name e.g. llama3.1:latest
        _client = OllamaChatClient(model=OLLAMA_MODEL, host=OLLAMA_HOST)
    return _client


def _extract_json_payload(raw_text: str) -> dict:
    """Parse model output even when wrapped in markdown or extra text."""
    text = (raw_text or "").strip()
    if not text:
        raise ValueError("Empty response text")
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        text = text[start : end + 1]
    return json.loads(text)


async def generate_slide_content(prompt: str, slide_count: int = 5) -> list[dict]:
    # New agent per request — Agent.run() accumulates history; a singleton would leak context across users/requests.
    agent = _get_client().as_agent(
        name="slide_writer",
        instructions=SYSTEM_PROMPT,
    )
    user_message = f"Topic: {prompt}. Slides: {slide_count}"
    response = await agent.run(user_message)
    raw = response.text
    if not raw.strip():
        raise RuntimeError("Ollama returned an empty response")

    parsed = _extract_json_payload(raw)
    slides = parsed.get("slides")
    if not isinstance(slides, list):
        raise RuntimeError("Response JSON missing 'slides' list")

    return slides
