import re
from io import BytesIO
from urllib.parse import quote

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

_SURROGATE_RE = re.compile(r"[\ud800-\udfff]")


def _safe_pptx_filename(prompt: str, max_stem: int = 30) -> str:
    """Build a safe .pptx filename from the user prompt (Windows/path-safe).

    May contain Unicode for RFC 5987 ``filename*`` (via
    ``_content_disposition_attachment``, which percent-encodes UTF-8 to ASCII).
    Never use this value alone in ``filename="..."``: Starlette encodes header
    values as Latin-1, and non-Latin-1 characters in that token would raise
    ``UnicodeEncodeError``.

    Strips lone surrogate code units so ``urllib.parse.quote`` cannot raise.
    """
    stem = (prompt or "").strip()[:max_stem]
    stem = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", stem)
    stem = _SURROGATE_RE.sub("_", stem)
    stem = stem.strip(" .") or "slides"
    return f"{stem}.pptx"


_ASCII_FILENAME_CHARS = re.compile(r"[^A-Za-z0-9._-]+")


def _ascii_fallback_pptx_filename(full_name: str, max_stem: int = 30) -> str:
    """Latin-1 / legacy ``filename=`` token: ASCII only so header encoding never fails."""
    lower = full_name.lower()
    stem = full_name[:-5] if lower.endswith(".pptx") else full_name
    stem = stem[:max_stem]
    stem = _ASCII_FILENAME_CHARS.sub("_", stem).strip("._- ") or "slides"
    return f"{stem}.pptx"


def _content_disposition_attachment(filename: str) -> str:
    """RFC 5987 attachment header: ASCII ``filename`` + UTF-8 ``filename*`` (pct-encoded).

    The full value must encode as Latin-1 (Starlette); this builder only emits
    ASCII after ``quote`` and ``_ascii_fallback_pptx_filename``.
    """
    fallback = _ascii_fallback_pptx_filename(filename)
    try:
        star = quote(filename, safe="")
    except UnicodeEncodeError:
        star = quote(fallback, safe="")
    hdr = f'attachment; filename="{fallback}"; filename*=UTF-8\'\'{star}'
    try:
        hdr.encode("latin-1")
    except UnicodeEncodeError:
        return 'attachment; filename="slides.pptx"; filename*=UTF-8\'\'slides.pptx'
    return hdr


@router.post("/generate")
async def generate_slides(req: SlideRequest):
    slides_data = await orch.run(req.prompt, req.slide_count)
    pptx_bytes = build_presentation(slides_data)
    filename = _safe_pptx_filename(req.prompt)
    return StreamingResponse(
        BytesIO(pptx_bytes),
        media_type=PPTX_MEDIA_TYPE,
        headers={"Content-Disposition": _content_disposition_attachment(filename)},
    )
