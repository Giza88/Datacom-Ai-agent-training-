from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.generate import router as generate_router
from routes.manim import router as manim_router
from routes.render import router as render_router

app = FastAPI(title="Slide Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_router)
app.include_router(manim_router)
app.include_router(render_router)

@app.get("/health")
def health():
    return {"status": "ok"}