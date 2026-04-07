from fastapi import APIRouter

router = APIRouter()


@router.post("/manim/render")
async def render_manim():
    """Stub — replace with real Manim pipeline later."""
    return {
        "video_url": "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "message": "Stub render — swap in generated file path",
    }
