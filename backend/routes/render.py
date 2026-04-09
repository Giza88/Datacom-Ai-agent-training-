from fastapi import APIRouter
from fastapi.responses import FileResponse
from services.manim_renderer import render_manim_scene

router = APIRouter()


@router.post("/render")
async def render(scene_class: str = "TitleSlide"):
    path = render_manim_scene(
        "manim_scenes/title_scene.py",
        scene_class,
        quality="l"
    )
    return FileResponse(path, media_type="video/mp4")
