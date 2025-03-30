from fastapi import APIRouter, HTTPException, Request
from src.nlu.analyzer import NLUAnalyzer
from utils.config_loader import load_config

nlu_router = APIRouter(prefix="/nlu")

nlu_config = load_config("./configs/nlu.yaml")

nlu = NLUAnalyzer(**nlu_config)

@nlu_router.post("/analyze")
async def analyze(request: Request) -> dict:
    try:
        data: dict = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid request data")
    results = await nlu.analyze(data)
    return results