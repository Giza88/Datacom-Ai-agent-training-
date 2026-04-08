import re
from io import BytesIO

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from services.ai_generator import generate_slide_content
from services.pptx_engine import build_presentation

router = APIRouter()

PPTX_MEDIA_TYPE = (
    "application/vnd.openxmlformats-officedocument.presentationml.presentation"
)


class SlideRequest(BaseModel):
    prompt: str
    slide_count: int = 5
    theme: str = "default"


def _safe_pptx_filename(prompt: str, max_stem: int = 30) -> str:
    """Build a safe .pptx filename from the user prompt (Windows/path-safe)."""
    stem = (prompt or "").strip()[:max_stem]
    stem = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", stem)
    stem = stem.strip(" .") or "slides"
    return f"{stem}.pptx"


@router.post("/generate")
async def generate_slides(req: SlideRequest):
    slides_data = await generate_slide_content(req.prompt, req.slide_count)
    pptx_bytes = build_presentation(slides_data)
    filename = _safe_pptx_filename(req.prompt)
    return StreamingResponse(
        BytesIO(pptx_bytes),
        media_type=PPTX_MEDIA_TYPE,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
