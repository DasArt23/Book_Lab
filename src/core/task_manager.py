import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Callable, List, Any, AsyncGenerator
from config import ExecutionMode


class TaskManager:
    """Централизованный управляющий компонент задач"""
    
    def __init__(self, mode: ExecutionMode = ExecutionMode.ASYNC, max_workers: int = 4):
        self.mode = mode
        self.max_workers = max_workers
        self._executor = None
        self._max_concurrent = max_workers * 2
    
    def start(self):
        """Создать executor"""
        if self.mode == ExecutionMode.THREAD:
            self._executor = ThreadPoolExecutor(max_workers=self.max_workers)
        elif self.mode == ExecutionMode.PROCESS:
            self._executor = ProcessPoolExecutor(max_workers=self.max_workers)
        return self
    
    def shutdown(self):
        """Закрыть executor"""
        if self._executor:
            self._executor.shutdown(wait=True)
    
    async def submit_heavy_task(self, task_func: Callable, *args, **kwargs) -> Any:
        """Отправляет тяжелую задачу в executor"""
        if self.mode == ExecutionMode.ASYNC:
            if asyncio.iscoroutinefunction(task_func):
                return await task_func(*args, **kwargs)
            else:
                return await asyncio.to_thread(task_func, *args, **kwargs)
        else:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(self._executor, task_func, *args, **kwargs)
    
    async def process_batch(self, task_func: Callable, items: List[Any], *args, **kwargs) -> AsyncGenerator:
        """Параллельная обработка батча задач с контролем параллелизма"""
        semaphore = asyncio.Semaphore(self._max_concurrent)

        async def process_with_limit(item):
            async with semaphore:
                return await self.submit_heavy_task(task_func, item, *args, **kwargs)
        tasks = [asyncio.create_task(process_with_limit(item)) for item in items]
        for task in asyncio.as_completed(tasks):
            yield await task
