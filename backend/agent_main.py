"""Container entrypoint: run the Slide Generator API (uvicorn).

Listens on 0.0.0.0. Port defaults to 8000; Azure Container Apps (and similar)
often set the PORT environment variable — that value is used when present.
"""
import os

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
