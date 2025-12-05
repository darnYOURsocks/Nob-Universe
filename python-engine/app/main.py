from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="NOB Universe Python Engine")


class AnalyzeRequest(BaseModel):
    payload: dict | None = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    return {
        "status": "processed",
        "received": request.payload or {},
        "summary": "Placeholder analysis from Python engine"
    }
