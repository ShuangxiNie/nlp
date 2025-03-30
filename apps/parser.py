from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import Optional
import os
import uuid
from io import BytesIO
from src.parser.docx_parser import convert_word2md
from .schema import ParseResponse

parser_router = APIRouter(prefix="/parser", tags=["文件解析"])

@parser_router.post("/upload")
async def parse(file: UploadFile = File(...)):
    print(file.filename)
    # 检查文件类型
    if not file.filename.endswith(('.txt', '.csv', '.json', '.pdf', '.docx', '.doc')):
        raise HTTPException(status_code=400, detail="支持多种文档")
    
    # 读取文件内容
    file_obj = await file.read()
    virtual_file = BytesIO(file_obj) # 转为文件对象

    # 不同的文件应该怎么转 MarkDown; TODO
    md_content = convert_word2md(virtual_file)
    
    # 示例：返回文件基本信息
    return ParseResponse(
        filename=file.filename,
        content=md_content.value
        # message=md_content.messages
    )