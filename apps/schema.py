from pydantic import BaseModel, Field
from typing import List, Optional

class Message(BaseModel):
    type: str
    message: str

# 解析结果定义
class ParseResponse(BaseModel):
    filename: str
    content: str
    # message: List[Message]

# embedding 的结果
class EmbeddingResponse(BaseModel):
    dense: List[float]

# 搜索的结果
class SearchResponse(BaseModel):
    filename: str
    collection_id: str
    content: str
    score: float
    rank: int