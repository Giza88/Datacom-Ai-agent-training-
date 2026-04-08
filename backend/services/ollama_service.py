"""Slide content via Ollama HTTP API: planner → parallel writers."""

from services.slide_pipeline import SlideOrchestrator


async def generate_slide_content(prompt: str, slide_count: int = 5) -> list[dict]:
    orchestrator = SlideOrchestrator()
    return await orchestrator.run(prompt, slide_count)
