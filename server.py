import uvicorn
import asyncio
import time
import logging
from fastapi import FastAPI, Request, HTTPException

from apps.nlu import nlu_router
from apps.parser import parser_router
from apps.embedding import emb_router

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

app = FastAPI()
# NLU 服务
app.include_router(nlu_router)

# 文档解析服务
app.include_router(parser_router)

# Embedding 服务
app.include_router(emb_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    # 使用字典的 setdefault 方法
    request.scope.setdefault("extensions", {})["process_time"] = process_time
    
    return response

@app.get("/")
def hello():
    return {"message": "Hello World"}



if __name__ == "__main__":
    uvicorn.run("server:app", 
                host="0.0.0.0", 
                port=8000, 
                reload=True,
                )