from data_processing.engine import Books_handler
from data_processing.source import Books_source
from domain.models import Book

class Application:
	def __init__(self):
		self.data_source = Books_source()
		self.data_handler = Books_handler()
	
	def run(self):
		raw_data = self.data_source.get_books()
		processed_data = self.data_handler.handler_books(raw_data)
		self.print_changes(raw_data, processed_data)
		print("Программа завершилась успешно")
	
	@staticmethod
	def print_changes(data1: list[Book], data2: list[Book]) -> None:
		for book1, book2 in zip(data1, data2):
			if(book1 != book2):
				print(book1)
				print(book2)
				print("Книги не одинаковы\n")
		print("Больше изменений нет")