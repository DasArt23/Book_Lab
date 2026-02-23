from domain.models import Book
from abc import ABC, abstractmethod


class Books_handler(ABC):
	name: str = "Handler"
	@abstractmethod
	def handler_books(self, books: list[Book]) -> list[Book]:
		pass
	
	@abstractmethod	
	def _handler_book(self, book: Book) -> Book:
		pass

class Text_handler(Books_handler):
	name = "Books Handler"
	def _handler_book(self, book: Book) -> Book:
		"""Обработка объекта Book и возврат его копии"""
		title = self.__clean_text(book.title, "Unknown Title")
		author = self.__clean_text(book.author, "Unknown Author")
		
		data = {
			"title": title, 
			"author": author,
			"recorder_id": book.recorder_id,
			"metadata": book.metadata.copy(),
			"favourite": book.favourite,
			"year": book.year,
		}
		
		return self.__create_copy(data)
		
	def handler_books(self, books: list[Book]) -> list[Book]:
		"""Обработка объектов Book"""
		return [self._handler_book(book) for book in books] if books else []
	
	@staticmethod
	def __clean_text(text: str, default: str) -> str:
		if not text or not text.strip():
			return default
		return " ".join(text.strip().split()).title()
	
	@staticmethod
	def __create_copy(data: dict) -> Book:
		new_book = Book(**data)
		return new_book
			