from manim import Scene, Text, Write, FadeIn, FadeOut, WHITE, BLUE, DOWN


class TitleSlide(Scene):
    """Animated title slide:
    1. Title text writes in char-by-char
    2. Subtitle fades in below
    3. Both fade out at end"""

    def construct(self):
        self.camera.background_color = "#0D1B2A"
        
        title = Text("AI Slide Generator", font_size=72, color=WHITE)
        subtitle = Text(
            "Powered by GPT-4o + python-pptx",
            font_size=36,
            color=BLUE
        )
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))
