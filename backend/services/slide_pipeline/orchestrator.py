import asyncio
import logging

import aiohttp

from services.ollama_client import OllamaClient

from .planner import PlannerAgent
from .writer import WriterAgent

logger = logging.getLogger(__name__)


class SlideOrchestrator:
    def __init__(self, ollama: OllamaClient | None = None) -> None:
        self._ollama = ollama or OllamaClient()
        self.planner = PlannerAgent(self._ollama)
        self.writer = WriterAgent(self._ollama)

    async def run(self, prompt: str, slide_count: int = 5) -> list[dict]:
        slide_count = max(1, slide_count)
        logger.info("Planning %s slides for: %s", slide_count, prompt)

        timeout = aiohttp.ClientTimeout(total=600)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            outline = await self.planner.run(session, prompt, slide_count)

            logger.info("Writing %s slides in parallel...", len(outline))

            slides = await asyncio.gather(
                *[self.writer.run(session, item) for item in outline]
            )

        logger.info("Done — %s slides ready.", len(slides))
        return list(slides)
