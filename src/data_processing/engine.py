from domain.models import Book

class Books_handler:
	def __init__(self):
		self.name = "Book Handler"
	
	def _handler_book(self, book: Book) -> Book:
		title = book.title
		title = self.__check_title(title)
		
		author = book.author
		author = self.__check_author(author)
		
		data = {
			"_title": title, 
			"_author": author,
			"_recorder_id": book.recorder_id,
			"_metadata": book.metadata,
			"_favourite": book.is_favourite(),
		}
		
		hbook = self.__create_copy(data)
		return hbook
		
	def handler_books(self, books: list[Book]) -> list[Book]:
		data = []
		if books is None:
			return []
		
		for book in books:
			hbook = self._handler_book(book)
			data.append(hbook)
		
		return data
	
	@staticmethod
	def __check_title(title: str) -> str:
		text = title.strip()
		if not text:
			text = "Unknown"
		else: 
			text = " ".join(text.split())
			text = text.title()
		return text
	
	@staticmethod
	def __check_author(author: str) -> str:
		new_author = author.strip()
		if not new_author:
			new_author = "Unknown"
		else:
			new_author = new_author.title()
		return new_author
	
	@staticmethod
	def __create_copy(data: dict) -> Book:
		new_book = Book(**data)
		return new_book
			