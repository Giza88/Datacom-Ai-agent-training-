import subprocess
import uuid
import os


def render_manim_scene(scene_file: str, scene_class: str, quality: str = "l") -> str:
    out = f"/tmp/{uuid.uuid4()}.mp4"
    cmd = [
        "manim",
        scene_file,
        scene_class,
        "-q", quality,
        "-o", out
    ]
    subprocess.run(cmd, check=True)
    return out
