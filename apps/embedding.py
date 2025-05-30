from typing import List
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, Request, HTTPException
from FlagEmbedding import BGEM3FlagModel
import time
import logging
from .schema import EmbeddingResponse, EmbeddingItem, UsageStats

logger = logging.getLogger("embedding")
emb_router = APIRouter(prefix="/v1")


# 初始化模型
start_time = time.time()
logger.info(f"BGEM3FlagModel start loading")
emb_model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
load_time = time.time() - start_time
logger.info(f"BGEM3FlagModel loaded finished in {load_time:.2f} seconds")

queue = asyncio.Queue()
executor = ThreadPoolExecutor(max_workers=2)  # 独立线程处理模型推理
max_batch_size = 32

async def batch_consumer():
    """消费者协程，处理批量请求"""
    max_batch_size = 32  # 最大批处理大小
    timeout = 0.01  # 等待批处理的最大时间（秒）
    
    while True:
        batch = []
        while len(batch) < max_batch_size and not queue.empty():
            item = await queue.get()
            batch.append(item)
        
        # 如果队列为空，等待更多请求
        if not batch:
            await asyncio.sleep(timeout)
            continue
        
        # 处理当前批次
        texts = [item["text"] for item in batch]
        futures = [item["future"] for item in batch]
        
        # 在单独线程中运行模型推理
        embeddings = await asyncio.get_event_loop().run_in_executor(
            executor, lambda: emb_model.encode(texts))
        
        # 处理 Batch 的问题
        dense_vecs = embeddings["dense_vecs"]

        # 设置结果到各个future
        for future, emb in zip(futures, dense_vecs):
            future.set_result(emb.tolist())  


@emb_router.post("/embeddings")
async def embedding(request: Request):
    """
    embedding 对外的接口
    """
    data = await request.json()
    # 后台异步处理
    future = asyncio.Future()
    await queue.put({"text": data["text"], "future": future})
    embedding = await future

    embedding_response = EmbeddingResponse(data=[EmbeddingItem(embedding=embedding, index=0)], 
                             object="list", 
                             usage=UsageStats(prompt_tokens=5, total_tokens=5))

    return embedding_response.model_dump()
