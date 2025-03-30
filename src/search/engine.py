from pymilvus import MilvusClient
from concurrent.futures import ThreadPoolExecutor
import asyncio
from asyncio import Queue, Future

class SearchEngine(object):
    def __init__(self) -> None:
        self.queue = Queue()
        self._excutor = ThreadPoolExecutor(max_workers=2)
        asyncio.create_task(self._update_index())

        self.dense = MilvusClient("./milvus_demo.db")

    async def insert(self, data):
        """
        向索引中插入数据
        """
        result = await self.dense.insert(data)

        return result
    

    async def _update_index(self):
        """
        索引更新协程
        """
        while True:
            if self.queue.empty():
                asyncio.sleep(1)

            item = await self.queue.get()
            data = item["data"]
            future = item["future"]
            
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor, lambda: self.insert(data))
            
            future.set_result(result)

    

    async def add_index(self, data):
        """
        对外暴露的接口
        """
        future = Future()
        await self.queue.put({"data": data, "future": future})
        result = await future
        return result
    

    async def search(**kwargs):
        """
        对外暴露的接口
        """
        
        pass


    async def rerank(items):
        return items
