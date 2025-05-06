import logging
import uvicorn
import asyncio
import time
from fastapi import FastAPI, Request, HTTPException
from contextlib import asynccontextmanager
from typing import List
from pydantic import BaseModel, Field

# 配置日志
from logging.handlers import TimedRotatingFileHandler

# 创建按天轮转的文件日志处理器
file_handler = TimedRotatingFileHandler(
    'app.log', when='midnight', interval=1, backupCount=7, encoding='utf-8'
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

# 控制台日志处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, file_handler]
)

from apps.embedding import batch_consumer as emb_batch_consumer

# 在 server.py 的 lifespan 函数中添加
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger("server")
    logger.info("Application starting up...")
    # 启动时需要执行的代码
    asyncio.create_task(emb_batch_consumer())
    yield
    # 关闭时需要执行的代码
    logger.info("Application shutting down...")
    await asyncio.sleep(10)

app = FastAPI(lifespan=lifespan)

# Embedding 服务
from apps.embedding import emb_router
app.include_router(emb_router)

# # NLU 服务
# from apps.nlu import nlu_router
# app.include_router(nlu_router)

# # 文档解析服务
# from apps.parser import parser_router
# app.include_router(parser_router)


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
                port=8000
                )