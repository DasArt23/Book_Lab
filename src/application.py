from data_processing.engine import Books_handler
from data_processing.source import Books_source
from domain.models import Book
from collections import defaultdict
from collections.abc import Iterable
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
	
	def run(self) -> None:
		print(f"Запуск в режиме: {self.config.execution_mode.value}")

		with ProcessTimer() as timer:
			self._process_sources_concurrent()

		dtime = timer.get_time()
		self.statistics.display()
		print(f"Время выполнения: {dtime:.3f} секунд")
		print("Программа завершилась успешно")

	async def run_async(self) -> None:
		print(f"Запуск в режиме: {self.config.execution_mode.value}")

		with ProcessTimer() as timer:
			await self._process_sources_async()

		dtime = timer.get_time()
		self.statistics.display()
		print(f"Время выполнения: {dtime:.3f} секунд")
		print("Программа завершилась успешно")

	def _process_sources_concurrent(self) -> None:
		for source in self.sources:
			for original, processed in self.mode_manager.execute(self.work_unit, source.get_books()):
				self.print_changes(original, processed, source.name)

	async def _process_sources_async(self) -> None:
		"""Асинхронная обработка источников"""
		tasks = (self._process_source_async(source) for source in self.sources)
		await asyncio.gather(*tasks)

	async def _process_source_async(self, source: Books_source) -> None:
		"""Асинхронная обработка одного источника"""
		async for original, processed in self.mode_manager.execute_async(self.work_unit, source.get_books_async()):
			await self._print_changes_async(original, processed, source.name)
			self.statistics.add_received(source.name, 1)
			if original != processed:
				self.statistics.add_modified(source.name, 1)

	# def process_source(self, source: Books_source) -> None:
	# 	raw_data = source.get_books()
	# 	if not raw_data:
	# 		print(f"Данные не получены")
	# 		return
	# 	processed_books = self.data_handler.handler_books(raw_data)
	# 	self.print_all_changes(processed_books, source.name)
	# def print_all_changes(self, proc_data: Iterable[tuple[Book, Book]], source_name: str) -> None:
	# 	for old, proc in proc_data:
	# 		self.print_changes(old, proc, source_name)
	
	def print_changes(self, old_book: Book, proc_book: Book, source_name: str) -> None:
		"""Сравнение атрибутов двух объектов Book"""
		self.statistics.add_received(source_name, 1)
		if old_book != proc_book:
			print("\nИзменения:")
			self.print_what_changed(old_book, proc_book)
			self.statistics.add_modified(source_name, 1)

	@staticmethod
	def print_what_changed(book1: Book, book2: Book) -> None:
		"""Вывод изменений объекта после обработки"""
		for attr, val1 in vars(book1).items():
			val2 = getattr(book2, attr)
			if val1 != val2:
				print(f"  {attr.title()}: {val1} -> {val2}")

	@staticmethod
	async def _print_changes_async(book1: Book, book2: Book, source_name: str) -> None:
		"""Асинхронный вывод изменений"""
		await asyncio.sleep(0.0001)
		if book1 != book2:
			print(f"\nИзменения {source_name}:")
			for attr, val1 in vars(book1).items():
				val2 = getattr(book2, attr)
				if val1 != val2:
					print(f"  {attr.title()}: {val1} -> {val2}")


class StatisticTracker():
	def __init__(self):
		self.received = defaultdict(int)
		self.modified = defaultdict(int)

	def add_received(self, source_name: str, count: int) -> None:
		self.received[source_name] += count

	def add_modified(self, source_name: str, count: int) -> None:
		self.modified[source_name] += count

	def display(self) -> None:
		for source in self.received.keys():
			print(f"Получено из источника {source}: {self.received[source]}")
			print(f"Изменено данных источника {source}: {self.modified[source]}\n")
