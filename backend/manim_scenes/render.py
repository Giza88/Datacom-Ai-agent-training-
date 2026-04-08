"""Manim CLI entry: import scenes here, then render by class name.

Run from ``backend/``::

    manim -pqh manim_scenes/render.py TitleSlide

Manim loads this file as a module; ensuring ``backend/`` is on ``sys.path`` keeps
``manim_scenes.title_slide`` imports reliable across Manim versions.
"""

from __future__ import annotations

import sys
from pathlib import Path

_backend_root = Path(__file__).resolve().parent.parent
if str(_backend_root) not in sys.path:
    sys.path.insert(0, str(_backend_root))

from manim_scenes.title_slide import TitleSlide

__all__ = ["TitleSlide"]
