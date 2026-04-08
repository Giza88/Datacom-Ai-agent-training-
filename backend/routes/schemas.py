from pydantic import BaseModel


class SlideRequest(BaseModel):
    prompt: str
    slide_count: int = 5
    theme: str = "default"
