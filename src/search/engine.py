from pymilvus import MilvusClient
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp
import asyncio
from asyncio import Queue, Future

class SearchEngine(object):
    def __init__(self) -> None:
        self.queue = Queue()
        
        # 进程池做搜索
        self._search_executor = mp.Pool(processes=2)

        # 线程池做索引更新
        self._index_executor = ThreadPoolExecutor(max_workers=2)

        asyncio.create_task(self._update_index())
        self.dense = MilvusClient("./milvus_demo.db")
    
    async def add_index(self, data):
        """
        对外暴露的接口
        """
        future = Future()
        await self.queue.put({"data": data, "future": future})
        result = await future
        return result

    async def _update_index(self):
        """
        索引更新协程, 后台进行更新
        """
        while True:
            try:
                if self.queue.empty():
                    asyncio.sleep(1)
                
                item = await self.queue.get()
                data = item["data"]
                future = item["future"]
                
                result = await asyncio.get_event_loop().run_in_executor(
                    self._index_executor, lambda: self.dense.insert(data))
                
                future.set_result(result)
            except Exception as e:
                print(f"索引更新失败: {e}")
                await asyncio.sleep(5)
    

    async def search(self, **kwargs):
        """
        对外暴露的搜索接口
        """
        return await asyncio.get_event_loop().run_in_executor(self._search_executor, 
                                        lambda: self.dense.search(**kwargs))


    async def rerank(items):
        return items


    async def close(self):
        """
        清理资源
        """
        self._executor.shutdown()
        await self.dense.close()

    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()