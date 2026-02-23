from data_processing.engine import Books_handler
from data_processing.source import Books_source
from domain.models import Book
from collections import defaultdict

class Application:
	def __init__(self, sources: list[Books_source], handler: Books_handler):
		self.name = "Application"
		self.sources = sources
		self.data_handler = handler
		
		self.amount_get = defaultdict(int)
		self.amount_changed = defaultdict(int)
	
	def run(self):
		for source in self.sources:
			raw_data = source.get_books()
			if not raw_data:
				print("Данные не получены")
			else:
				amount = len(raw_data)
				self.amount_get[source.name] += amount
				print(f"Получено данных: {amount}")
				processed_data = self.data_handler.handler_books(raw_data)
				self.print_changes(raw_data, processed_data, source.name)
		
		self.print_amount_get_changes()
		print("Программа завершилась успешно")
	
	def print_changes(self, data1: list[Book], data2: list[Book], source_name: str) -> None:
		c = 0
		for book1, book2 in zip(data1, data2):
			if(book1 != book2):
				print("\nИзменения:")
				self.print_what_changed(book1, book2)
				c += 1
		self.amount_changed[source_name] += c
		print("\nБольше изменений нет")
		print(f"Количетсов изменений: {c}")
	
	def print_amount_get_changes(self) -> None:
		for source_name in self.amount_get.keys():
			print(f"Получено из источника {source_name}: {self.amount_get[source_name]}")
			print(f"Изменено данных источника {source_name}: {self.amount_changed[source_name]}\n")

	@staticmethod
	def print_what_changed(book1: Book, book2: Book) -> None:
		attrs = book1.__dict__.keys()
		for attr in attrs:
			val1, val2 = getattr(book1, attr), getattr(book2, attr)
			title = attr.title()
			if val1 != val2:
				print(f"{title}: {val1} -> {val2}")