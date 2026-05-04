from domain.models import Book
from abc import ABC, abstractmethod
from dataclasses import replace
from datetime import datetime
from collections.abc import Iterable
from typing import Generator


class Books_handler(ABC):
	name: str = "Handler"

	@abstractmethod
	def handler_book(self, book: Book) -> Book:
		pass

	def handler_books(self, books: Iterable[Book]) -> Generator[tuple[Book, Book], None, None]:
		"""Возвращает генератор с кортежами (old_book, new_book)"""
		for book in books:
			yield book, self.handler_book(book)

	@staticmethod
	def create_copy(book: Book, **kwargs) -> Book:
		kwargs["metadata"] = book.metadata.copy() if "metadata" not in kwargs else kwargs["metadata"].copy()
		return replace(book, **kwargs)

class Text_handler(Books_handler):
	name = "Books Text Handler"

	def __init__(self, **kwargs):
		pass

	def handler_book(self, book: Book) -> Book:
		"""Обработка объекта Book и возврат его копии"""
		return self.create_copy(
			book,
			title = self.clean_text(book.title, "Unknown Title"),
			author = self.clean_text(book.author, "Unknown Author"),
		)

	@staticmethod
	def clean_text(text: str, default: str) -> str:
		if not text or not text.strip():
			return default
		return " ".join(text.strip().split()).title()

class Year_handler(Books_handler):
	name = "Books Year Handler"

	def __init__(self, treshold=2, **kwargs):
		self.treshold = treshold

	def handler_book(self, book: Book) -> Book:
		"""Обновляет метаданные, помечая новинки"""
		updated_metadata = book.metadata.copy()
		cur_year = self.get_cur_year()
		updated_metadata['modern'] = book.year >= cur_year - self.treshold
		return self.create_copy(
				book,
				year=min(book.year, cur_year),
				metadata = updated_metadata,
		)

	@staticmethod
	def get_cur_year() -> int:
		return datetime.now().year

class ID_handler(Books_handler):
	name = "Books RecorderID Handler"

	def __init__(self, rec_id=0, **kwargs):
		self.rec_id = rec_id

	def handler_book(self, book: Book):
		return self.create_copy(
			book,
			recorder_id = self.rec_id,
		)



