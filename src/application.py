from data_processing.engine import Books_handler
from data_processing.source import Books_source
from domain.models import Book
from collections import defaultdict

class Application:
	def __init__(self, sources: list[Books_source], handler: Books_handler):
		self.sources = sources
		self.data_handler = handler
		self.statistics = StatisticTracker()
	
	def run(self) -> None:
		"""Основной цикл программы"""
		for source in self.sources:
			self.process_source(source)

		self.statistics.display()
		print("Программа завершилась успешно")

	def process_source(self, source: Books_source) -> None:
		raw_data = source.get_books()

		if not raw_data:
			print("Данные не получены")
			return

		self.statistics.add_received(source.name, len(raw_data))
		print(f"Получено данных: {len(raw_data)}")

		proccesed_data = self.data_handler.handler_books(raw_data)
		self.print_changes(raw_data, proccesed_data, source.name)
	
	def print_changes(self, data1: list[Book], data2: list[Book], source_name: str) -> None:
		"""Сравнение атрибутов двух объектов Book"""
		c = 0
		for book1, book2 in zip(data1, data2):
			if book1 != book2:
				print("\nИзменения:")
				self.print_what_changed(book1, book2)
				c += 1
		self.statistics.add_modified(source_name, c)
		print(f"Количество изменений: {c}")

	@staticmethod
	def print_what_changed(book1: Book, book2: Book) -> None:
		"""Вывод изменений объекта после обработки"""
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
