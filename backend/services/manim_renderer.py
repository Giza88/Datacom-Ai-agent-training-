import subprocess
import os


def render_manim_scene(
    scene_file: str,
    scene_class: str,
    quality: str = "l"
) -> str:
    """Runs Manim CLI as a subprocess and returns output path.
    quality: 'l' = low/fast (480p) | 'h' = high (1080p)
    """

    result = subprocess.run(
        ["manim", f"-q{quality}", scene_file, scene_class],
        capture_output=True,
        text=True,
        timeout=120
    )

    if result.returncode != 0:
        raise RuntimeError(f"Manim failed:\n{result.stderr}")

    base = os.path.splitext(os.path.basename(scene_file))[0]
    resolution = "480p15" if quality == "l" else "1080p60"
    output = f"media/videos/{base}/{resolution}/{scene_class}.mp4"

    if not os.path.exists(output):
        raise FileNotFoundError(f"Output missing: {output}")

    return output
