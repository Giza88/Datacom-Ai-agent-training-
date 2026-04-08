"""Sanity check: Ollama HTTP API reachable (run from backend/: python smoke_ollama_agent.py)."""
import asyncio

import aiohttp

from config import OLLAMA_HOST


async def main() -> None:
    base = OLLAMA_HOST.rstrip("/")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base}/api/tags") as resp:
            resp.raise_for_status()
            data = await resp.json()
        models = data.get("models") or []
        print(f"Ollama OK at {base} — {len(models)} model(s) in library.")


if __name__ == "__main__":
    asyncio.run(main())
