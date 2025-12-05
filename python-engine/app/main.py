from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Nob-Universe Python Engine")


class PatternRequest(BaseModel):
    seed: int | None = None


class PatternResponse(BaseModel):
    id: str
    name: str
    description: str


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate", response_model=PatternResponse)
async def generate_pattern(payload: PatternRequest) -> PatternResponse:
    seed = payload.seed or 0
    base_patterns = [
        PatternResponse(id="pattern-spiral", name="Spiral", description="Logarithmic spiral"),
        PatternResponse(id="pattern-grid", name="Grid", description="Axis-aligned grid"),
        PatternResponse(id="pattern-wave", name="Wave", description="Sine wave variation"),
    ]
    choice = base_patterns[seed % len(base_patterns)]
    return choice


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Nob-Universe Python Engine"}
