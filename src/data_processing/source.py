from domain.models import Book
from abc import ABC, abstractmethod
from wonderwords import RandomWord
from pathlib import Path
import random
import string
import json

class Books_source(ABC):
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
	
	def __init__(self, path: str = 'file.json'):
		self.path = Path(__file__).parent / path
	
	def get_books(self) -> list[Book]:
		data, sl = [], dict()
		
		if not self.__check_path():
			return data
		
		with open(self.path, 'r', encoding='utf-8') as file:
			sl = json.load(file)
			
		for title in sl.keys():
			book_js = sl[title]
			book_js['title'] = title
			book = Book(**{f"_{k}": v for k, v in book_js.items()})
			book.set_source(self._name)
			data.append(book)
		return data
	
	def __check_path(self) -> bool:
		file = Path(self.path)
		if file.is_file():
			return True
		return False

class Rand_source(Books_source):
	_name = "Random source"
	_source_type = "generator"
	
	def __init__(self, amount: int = 1, title_len: int = 10):
		self.amount = max(amount, 1)
		self.title_len = max(title_len, 1)
		
	def __get_rand_title(self) -> str:
		r = RandomWord()
		title = r.word(include_categories=["adjective"]) + " " + r.word(include_categories=['noun'])
		return title
	
	@staticmethod
	def __get_rand_id() -> int:
		return random.randint(1000, 10000)
	
	@staticmethod
	def __get_rand_author() -> str:
		l1, l2 = random.choice(string.ascii_letters), random.choice(string.ascii_letters)
		word = RandomWord().word(include_categories=['noun'])
		return f"{l1}. {l2}. {word}"
	
	def get_books(self) -> list[Book]:
		books = [0]*self.amount
		for i in range(self.amount):
			books[i] = Book(
				_title = self.__get_rand_title(),
				_recorder_id = self.__get_rand_id(),
				_author = self.__get_rand_author(),
			)
			books[i].set_source(self._name)
		return books

class Demo_source(Books_source):
	def get_books(self) -> list[Book]:
		books_list = [
			Book(
				_title="The War   of the Worlds",
				_recorder_id=123,
				_author="H.G. Wells",
			),
			Book(
				_title="Вишневый Сад",
				_recorder_id=100,
				_author="А.П. чехов",
			),
		]
		for book in books_list:
			book.set_source(self._name) 
		return books_list