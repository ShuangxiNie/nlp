from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Message(BaseModel):
    type: str
    message: str

# 解析结果定义
class ParseResponse(BaseModel):
    filename: str
    content: str
    # message: List[Message]

# embedding 的结果
class EmbeddingItem(BaseModel):
    embedding: List[float]
    index: int=0
    object: str = "embedding"  # 设置默认值

class UsageStats(BaseModel):
    prompt_tokens: int=0
    total_tokens: int=0

class EmbeddingResponse(BaseModel):
    data: List[EmbeddingItem]
    model: str="bge_m3"
    object: str = "list"  # 设置默认值
    usage: UsageStats

# 搜索的结果
class SearchResponse(BaseModel):
    filename: str
    collection_id: str
    content: str
    score: float
    rank: int