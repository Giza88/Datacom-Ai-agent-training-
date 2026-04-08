"""One-shot check that Ollama + Agent Framework respond (run from repo: python smoke_ollama_agent.py)."""
import asyncio

from agent_framework.ollama import OllamaChatClient

from config import OLLAMA_HOST, OLLAMA_MODEL


async def main() -> None:
    client = OllamaChatClient(model=OLLAMA_MODEL, host=OLLAMA_HOST)
    agent = client.as_agent(
        name="smoke",
        instructions="Reply with exactly one short sentence.",
    )
    response = await agent.run("Say hello.")
    print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
