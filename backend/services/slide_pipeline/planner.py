import aiohttp

from services.llm_utils import extract_json_payload
from services.ollama_client import OllamaClient

PLANNER_INSTRUCTIONS = """You are a presentation architect.
Given a topic and slide count, return ONLY valid JSON:
{"outline": [{"slide_number": 1, "title": "...", "focus": "one sentence"}]}
No markdown. JSON only.
The outline must have exactly the requested number of slides, slide_number 1..N, ordered logically."""


class PlannerAgent:
    def __init__(self, client: OllamaClient | None = None) -> None:
        self._ollama = client if client is not None else OllamaClient()

    async def run(
        self,
        session: aiohttp.ClientSession,
        prompt: str,
        slide_count: int,
    ) -> list[dict]:
        user_message = (
            f"{PLANNER_INSTRUCTIONS}\n\nTopic: {prompt}. Slides: {slide_count}"
        )
        raw = await self._ollama.generate(session, user_message)
        if not raw.strip():
            raise RuntimeError("Planner returned an empty response")

        parsed = extract_json_payload(raw)
        outline = parsed.get("outline")
        if not isinstance(outline, list) or len(outline) == 0:
            raise RuntimeError("Planner JSON missing non-empty 'outline' list")

        normalized: list[dict] = []
        for i, item in enumerate(outline, start=1):
            if not isinstance(item, dict):
                raise RuntimeError("Each outline entry must be an object")
            normalized.append(
                {
                    "slide_number": int(item.get("slide_number", i)),
                    "title": str(item.get("title", "")).strip() or f"Slide {i}",
                    "focus": str(item.get("focus", "")).strip(),
                }
            )

        if len(normalized) != slide_count:
            if len(normalized) > slide_count:
                normalized = normalized[:slide_count]
            else:
                while len(normalized) < slide_count:
                    j = len(normalized) + 1
                    normalized.append(
                        {
                            "slide_number": j,
                            "title": f"Slide {j}",
                            "focus": prompt,
                        }
                    )

        return normalized
