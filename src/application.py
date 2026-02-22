from data_processing.engine import Books_handler
from data_processing.source import Books_source
from domain.models import Book

class Application:
	def __init__(self):
		self.name = "Application"
	
	def run(self):
		data_source = Books_source()
		data_handler = Books_handler()
		
		raw_data = data_source.get_books()
		if not raw_data:
			print("Данные не получены")
		else:
			amount = len(raw_data)
			print(f"Получено данных: {amount}")
			processed_data = data_handler.handler_books(raw_data)
			self.print_changes(raw_data, processed_data)
		print("Программа завершилась успешно")
	
	def print_changes(self, data1: list[Book], data2: list[Book]) -> None:
		c = 0
		for book1, book2 in zip(data1, data2):
			if(book1 != book2):
				print("\nИзменения:")
				self.print_what_changed(book1, book2)
				c += 1
		print("\nБольше изменений нет")
		print(f"Количетсов изменений: {c}")
	
	@staticmethod
	def print_what_changed(book1: Book, book2: Book) -> None:
		attrs = book1.__dict__.keys()
		for attr in attrs:
			val1, val2 = getattr(book1, attr), getattr(book2, attr)
			title = attr.title()
			if val1 != val2:
				print(f"{title}: {val1} -> {val2}")