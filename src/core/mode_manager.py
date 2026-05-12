# core/mode_manager.py
from config import ExecutionMode
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Callable, List, Any, Generator


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
