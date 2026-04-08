import re
from io import BytesIO

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from .orchestrator import SlideOrchestrator
from .ppt_builder import build_presentation
from .schemas import SlideRequest

router = APIRouter()
orch = SlideOrchestrator()

PPTX_MEDIA_TYPE = (
    "application/vnd.openxmlformats-officedocument.presentationml.presentation"
)


def _safe_pptx_filename(prompt: str, max_stem: int = 30) -> str:
    """Build a safe .pptx filename from the user prompt (Windows/path-safe)."""
    stem = (prompt or "").strip()[:max_stem]
    stem = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", stem)
    stem = stem.strip(" .") or "slides"
    return f"{stem}.pptx"


@router.post("/generate")
async def generate_slides(req: SlideRequest):
    slides_data = await orch.run(req.prompt, req.slide_count)
    pptx_bytes = build_presentation(slides_data)
    filename = _safe_pptx_filename(req.prompt)
    return StreamingResponse(
        BytesIO(pptx_bytes),
        media_type=PPTX_MEDIA_TYPE,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
