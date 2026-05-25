from data_processing.engine import Books_handler
from data_processing.source import Books_source
from domain.models import Book
from collections import defaultdict
from collections.abc import Iterable, Generator, AsyncGenerator
from config import AppConfig
from core.mode_manager import ModeManager
from core.timer import ProcessTimer
from domain.work_unit import BookWorkUnit
import asyncio


class Application:
    def __init__(self, sources: Iterable[Books_source], handler: Books_handler):
        self.sources = sources
        self.data_handler = handler
        self.statistics = StatisticTracker()
        self.config = AppConfig()
        self.mode_manager = ModeManager(
            mode=self.config.execution_mode,
            max_workers=self.config.max_workers,
        )
        self.work_unit = BookWorkUnit(self.data_handler)

    def run(self) -> Generator[tuple[Book, Book], None, None]:
        print(f"Запуск в режиме: {self.config.execution_mode.value}")

        with ProcessTimer() as timer:
            for source in self.sources:
                for original, processed in self.mode_manager.execute(self.work_unit, source.get_books()):
                    self.print_changes(original, processed, source.name)
                    yield original, processed

        dtime = timer.get_time()
        self.statistics.display()
        print(f"Время выполнения: {dtime:.3f} секунд")
        print("Программа завершилась успешно")

    async def run_async(self) -> AsyncGenerator[tuple[Book, Book], None]:
        print(f"Запуск в режиме: {self.config.execution_mode.value}")

        with ProcessTimer() as timer:
            for source in self.sources:
                async for original, processed in self.mode_manager.execute_async(self.work_unit, source.get_books_async()):
                    await self._print_changes_async(original, processed, source.name)
                    self.statistics.add_received(source.name, 1)
                    if original != processed:
                        self.statistics.add_modified(source.name, 1)
                    yield original, processed

        dtime = timer.get_time()
        self.statistics.display()
        print(f"Время выполнения: {dtime:.3f} секунд")
        print("Программа завершилась успешно")

    async def run_hybrid(self) -> AsyncGenerator[tuple[Book, Book], None]:
        print(f"Запуск в режиме: {self.config.execution_mode.value}")

        with ProcessTimer() as timer:
            for source in self.sources:
                books = []
                async for book in source.get_books_async():
                    books.append(book)

                async for original, processed in self.mode_manager.execute_hybrid(self.work_unit, books):
                    await self._print_changes_async(original, processed, source.name)
                    self.statistics.add_received(source.name, 1)
                    if original != processed:
                        self.statistics.add_modified(source.name, 1)
                    yield original, processed

        dtime = timer.get_time()
        self.statistics.display()
        print(f"Время выполнения: {dtime:.3f} секунд")
        print("Программа завершилась успешно")

    def print_changes(self, old_book: Book, proc_book: Book, source_name: str) -> None:
        self.statistics.add_received(source_name, 1)
        if old_book != proc_book:
            print("\nИзменения:")
            self.print_what_changed(old_book, proc_book)
            self.statistics.add_modified(source_name, 1)

    @staticmethod
    def print_what_changed(book1: Book, book2: Book) -> None:
        for attr, val1 in vars(book1).items():
            val2 = getattr(book2, attr)
            if val1 != val2:
                print(f"  {attr.title()}: {val1} -> {val2}")

    @staticmethod
    async def _print_changes_async(book1: Book, book2: Book, source_name: str) -> None:
        await asyncio.sleep(0.0001)
        if book1 != book2:
            print(f"\nИзменения {source_name}:")
            for attr, val1 in vars(book1).items():
                val2 = getattr(book2, attr)
                if val1 != val2:
                    print(f"  {attr.title()}: {val1} -> {val2}")


class StatisticTracker:
    def __init__(self):
        self.received = defaultdict(int)
        self.modified = defaultdict(int)

    def add_received(self, source_name: str, count: int) -> None:
        self.received[source_name] += count

    def add_modified(self, source_name: str, count: int) -> None:
        self.modified[source_name] += count

    def get_stat(self) -> str:
        text = ""
        for source in self.received.keys():
            text += f"Получено из источника {source}: {self.received[source]}\n"
            text += f"Изменено данных источника {source}: {self.modified[source]}\n\n"
        return text

    def display(self) -> None:
        print(self.get_stat())
