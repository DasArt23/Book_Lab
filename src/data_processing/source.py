from domain.models import Book
from abc import ABC, abstractmethod
from wonderwords import RandomWord
from pathlib import Path
import random
import string
import json

class Books_source(ABC):
	"""Базовый интерфейс источника данных"""
	_name = "Demo source"
	_source_type = "demo"
	
	@property
	def source_type(self) -> str:
		return self._source_type
	
	@property
	def name(self) -> str:
		return self._name
	
	@abstractmethod
	def get_books(self) -> list[Book]:
		pass

class FileJSON_source(Books_source):
	_name = "JSON source"
	_source_type = "json"
	
	def __init__(self, path: str = 'json_files/file.json'):
		self.path = (Path(__file__).parent / path).resolve()
	
	def get_books(self) -> list[Book]:
		data, sl = [], dict()
		
		if not self.path.is_file():
			return []
		
		try:
			with open(self.path, 'r', encoding='utf-8') as file:
				sl = json.load(file)
		except (json.JSONDecodeError, OSError):
			return []
			
		for title in sl.keys():
			book_js = sl[title]
			book_js['title'] = title
			book = Book(**book_js).set_source(self._name)
			data.append(book)
		return data

class Rand_source(Books_source):
	_name = "Random source"
	_source_type = "generator"
	
	def __init__(self, amount: int = 1):
		self.amount = max(amount, 1)
		self.rw = RandomWord()
		
	def __get_rand_title(self) -> str:
		title = self.rw.word(include_categories=["adjective"]) + " " + self.rw.word(include_categories=['noun'])
		return title
	
	@staticmethod
	def __get_rand_id() -> int:
		return random.randint(1000, 10000)
	
	def __get_rand_author(self) -> str:
		l1, l2 = random.choice(string.ascii_letters), random.choice(string.ascii_letters)
		word = self.rw.word(include_categories=['noun'])
		return f"{l1}. {l2}. {word}"
	
	def get_books(self) -> list[Book]:
		return [
			Book(
				title = self.__get_rand_title(),
				recorder_id = self.__get_rand_id(),
				author = self.__get_rand_author()
			).set_source(self._name)
			for _ in range(self.amount)
		]

class Demo_source(Books_source):
	def get_books(self) -> list[Book]:
		books_list = [
			Book(
				title="The War   of the Worlds",
				recorder_id=123,
				author="H.G. Wells",
			).set_source(self._name),
			Book(
				title="Вишневый Сад",
				recorder_id=100,
				author="А.П. чехов",
			).set_source(self._name),
		]
		return books_list