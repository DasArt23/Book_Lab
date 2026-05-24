# core/mode_manager.py
from config import ExecutionMode
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Callable, List, Any, Generator, AsyncGenerator
import asyncio


class ModeManager:
    """Менеджер режимов выполнения"""
    def __init__(self, mode: ExecutionMode = ExecutionMode.SEQUENTIAL, max_workers: int = 4):
        self.mode = mode
        self.max_workers = max_workers

    def execute(self, task_func: Callable, items: List[Any], *args, **kwargs) -> Generator:
        """Выполняет задачи в выбранном режиме
            task_func: единица работы
            items: список элементов для обработки
            *args, **kwargs: аргументы для task_func
        """
        if self.mode == ExecutionMode.SEQUENTIAL:
            yield from self._run_sequential(task_func, items, *args, **kwargs)
        elif self.mode == ExecutionMode.THREAD:
            yield from self._run_thread_pool(task_func, items, *args, **kwargs)
        elif self.mode == ExecutionMode.PROCESS:
            yield from self._run_process_pool(task_func, items, *args, **kwargs)
        elif self.mode == ExecutionMode.ASYNC:
            raise RuntimeError("Для async режима используйте execute_async")

    async def execute_async(self, task_func: Callable, items: AsyncGenerator, *args, **kwargs) -> AsyncGenerator:
        tasks = [asyncio.create_task(self._run_async_task(task_func, item, *args, **kwargs)) async for item in items]
        for task in asyncio.as_completed(tasks):
            yield await task

    async def _run_async_task(self, task_func, item, *args, **kwargs):
        """Запуск асинхронной задачи"""
        if hasattr(task_func, '__call_async__'):
            return await task_func.__call_async__(item, *args, **kwargs)
        else:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, task_func, item, *args, **kwargs)

    def _run_sequential(self, task_func, items, *args, **kwargs):
        """Последовательно"""
        for item in items:
            yield task_func(item, *args, **kwargs)

    def _run_thread_pool(self, task_func, items, *args, **kwargs):
        """Потоковый пул"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(task_func, item, *args, **kwargs) for item in items]
            for future in futures:
                yield future.result()

    def _run_process_pool(self, task_func, items, *args, **kwargs):
        """Процессный пул"""
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(task_func, item, *args, **kwargs) for item in items]
            for future in futures:
                yield future.result()

    async def execute_hybrid(self, task_func: Callable, items: List[Any], *args, **kwargs) -> AsyncGenerator:
        from core.task_manager import TaskManager
        tm = TaskManager(mode=self.mode, max_workers=self.max_workers)
        tm.start()
        try:
            async for result in tm.process_batch(task_func, items, *args, **kwargs):
                yield result
        finally:
            tm.shutdown()
