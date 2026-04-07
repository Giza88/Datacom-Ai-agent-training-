from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from io import BytesIO

router = APIRouter()


class SlideRequest(BaseModel):
    prompt: str
    slide_count: int = 5
    theme: str = "default"


@router.post("/generate")
async def generate_slides(req: SlideRequest):
    # Stub — replaced with real pptx service on Slide 14
    return {"message": f"Will build {req.slide_count} slides for: {req.prompt}"}
