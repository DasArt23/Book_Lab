from domain.models import Book
from abc import ABC, abstractmethod
from wonderwords import RandomWord
from pathlib import Path
from typing import Generator
import random
import string
import ijson

class Books_source(ABC):
	"""Базовый интерфейс источника данных"""
	_name = "Demo source"
	_source_type = "demo"

	def __init__(self, **kwargs):
		pass
	
	@property
	def source_type(self) -> str:
		return self._source_type
	
	@property
	def name(self) -> str:
		return self._name
	
	@abstractmethod
	def get_books(self) -> Generator[Book, None, None]:
		pass

class FileJSON_source(Books_source):
	_name = "JSON source"
	_source_type = "json"
	
	def __init__(self, path: str = 'json_files/file.json', **kwargs):
		self.path = (Path(__file__).parent / path).resolve()

	def get_books(self) -> Generator[Book, None, None]:
		for title, book_js in self._get_items():
			yield Book(title=title, **book_js).set_source(self._name)

	def _get_items(self) -> Generator[tuple[str, dict], None, None]:
		if not self.path.is_file():
			return
		try:
			with open(self.path, 'rb') as file:
				yield from ijson.kvitems(file, '')
		except (ijson.common.IncompleteJSONError, OSError):
			return


class Rand_source(Books_source):
	_name = "Random source"
	_source_type = "generator"
	
	def __init__(self, amount: int = 1, **kwargs):
		self.amount = max(amount, 1)
		self.rw = RandomWord()
		
	def get_rand_title(self) -> str:
		title = self.rw.word(include_categories=["adjective"]) + " " + self.rw.word(include_categories=['noun'])
		return title
	
	@staticmethod
	def get_rand_id() -> int:
		return random.randint(1000, 10000)
	
	@staticmethod
	def get_rand_year() -> int:
		return random.randint(1600, 3000)
	
	def get_rand_author(self) -> str:
		l1, l2 = random.choice(string.ascii_letters), random.choice(string.ascii_letters)
		word = self.rw.word(include_categories=['noun'])
		return f"{l1}. {l2}. {word}"

	def get_books(self) -> Generator[Book, None, None]:
		for _ in range(self.amount):
			yield Book(
					title = self.get_rand_title(),
					recorder_id = self.get_rand_id(),
					author = self.get_rand_author(),
					year = self.get_rand_year(),
				).set_source(self._name)

class Demo_source(Books_source):
	def get_books(self) -> Generator[Book, None, None]:
		books_list = [
			Book(
				title="The War   of the Worlds",
				recorder_id=123,
				author="H.G. Wells",
				year=1897,
			).set_source(self._name),
			Book(
				title="Вишневый Сад",
				recorder_id=100,
				author="А.П. чехов",
				year=20012,
			).set_source(self._name),
		]
		yield from (book for book in books_list)
