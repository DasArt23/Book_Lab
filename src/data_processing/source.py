from domain.models import Book

class Books_source:
	def __init__(self):
		self.name = "Proba"
		self._source_type = "Test"
	
	def get_type(self):
		return self._source_type
	
	def get_books(self) -> list[Book]:
		books_list = [
			Book(
				title="The War   of the Worlds",
				recorder_id=123,
				author="H.G. Wells",
			),
			Book(
				title="  Вишневый сад",
				recorder_id=100,
				author="А.П. чехов",
			)
		]
		return books_list