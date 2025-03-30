import asyncio
import torch
from pydantic import BaseModel
from transformers import BertTokenizer, BertModel

# 初始化 BERT 模型和分词器
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
model.eval()

# 批量处理参数
BATCH_SIZE = 16
TIME_WINDOW = 0.1  # 100毫秒

# 请求队列
request_queue = []

async def process_batch():
    while True:
        await asyncio.sleep(TIME_WINDOW)
        if request_queue:
            batch = request_queue[:BATCH_SIZE]
            del request_queue[:BATCH_SIZE]
            
            texts = [item['text'] for item in batch]
            inputs = tokenizer(texts, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                outputs = model(**inputs)
            
            for i, item in enumerate(batch):
                item['future'].set_result(outputs.last_hidden_state[i].numpy().tolist())