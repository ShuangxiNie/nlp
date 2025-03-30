from fastapi import APIRouter, Request, HTTPException
import asyncio
from src.search import SearchEngine

search_router = APIRouter(prefix="/search")

search_engine = SearchEngine()

@search_router.post()
async def search(request: Request):
    data = await request.json()

    results = await search_engine.work(data)

    return results


@search_router.post("/insert")
async def insert(request: Request):
    data = await request.json()

    result = await search_engine.add_index(data)

    return result

    

