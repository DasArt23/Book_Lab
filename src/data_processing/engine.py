from domain.models import Book

class Books_handler:
	def __init__(self):
		self.name = "Book Handler"
	
	def _handler_book(self, book: Book) -> Book:
		title = book.get_title()
		title = self.__check_title(title)
		
		author = book.get_author()
		author = self.__check_author(author)
		
		data = {
			"title": title,
			"author": author,
			"recorder_id": book.get_rec_id(),
			"metadata": book.get_metadata(),
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
		text = title
		if not title:
			text = "Unknown"
		else: 
			text = text.title().strip()
		return text
	
	@staticmethod
	def __check_author(author: str) -> str:
		new_author = author
		if not new_author:
			new_author = "Unknown"
		else:
			new_author = new_author.title().strip()
		return new_author
	
	@staticmethod
	def __create_copy(data) -> Book:
		new_book = Book(**data)
		return new_book
			