from domain.models import Book
from abc import ABC, abstractmethod
from wonderwords import RandomWord
from pathlib import Path
from typing import Generator, AsyncGenerator
from bs4 import BeautifulSoup, PageElement
from config import AppConfig
from core.error_handler import ErrorHandler, FetchError
from core.rate_limiter import RateLimiter
import random
import string
import ijson
import asyncio
import httpx


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

	async def get_books_async(self) -> AsyncGenerator[Book, None]:
		for book in self.get_books():
			await asyncio.sleep(0.01)
			yield book


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


class Parse_source(Books_source):
	_name = "Parse source"

	def __init__(self, urls: list[str], **kwargs):
		self.urls = urls
		self.config = AppConfig()
		self._rate_limiter = RateLimiter()
		self._error_handler = ErrorHandler(self._rate_limiter)
		self.queuePages = asyncio.Queue(1)
		self.queueBooks = asyncio.Queue(100)
		self._stop_marker = object()
		self._failed_urls = []
		self._successful_urls = []

	def get_books(self) -> Generator[Book, None, None]:
		yield from Demo_source().get_books()

	@staticmethod
	def get_book(book_element: PageElement):
		data = book_element.findAll('a')[1]
		title = data['title']
		url = data['href']
		return title, {'url': url}

	async def parse_books(self, page_text: str) -> None:
		soup = BeautifulSoup(page_text, "html.parser")
		books = soup.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
		for book in books:
			await asyncio.sleep(0.01)
			title, data = self.get_book(book)
			await self.queueBooks.put(Book(title=title, **data))

	async def get_page_async(self) -> AsyncGenerator[str, None]:
		timeout = httpx.Timeout(
			connect=5.0,
			read=self.config.request_timeout,
			write=5.0,
			pool=2.0,
		)

		print(f"max_concurrent={self.config.max_concurrent_requests} delay={self.config.request_delay}s retry={self.config.retry_count}")

		async def producer():
			try:
				async with httpx.AsyncClient(timeout=timeout) as client:
					async def get(u):
						try:
							page_text = await self._error_handler.fetch_with_retry(client, u, self._rate_limiter)
							if page_text:
								await self.queuePages.put(page_text)
								self._successful_urls.append(u)
							else:
								self._failed_urls.append(u)
								await self.queuePages.put(self._stop_marker)
						except FetchError as e:
							print(f"Failed {u}: {e.message}")
							self._failed_urls.append(u)

					await asyncio.gather(*(get(u) for u in self.urls))
			finally:
				await self.queuePages.put(self._stop_marker)

		task = asyncio.create_task(producer())
		c = 0
		try:
			while True:
				try:
					page = await asyncio.wait_for(self.queuePages.get(), timeout=30.0)
				except asyncio.TimeoutError:
					print("Timeout waiting for page")
					break

				if page is self._stop_marker:
					print("Stop marker received")
					break

				if page is None:
					continue

				c += 1
				print(f"Page {c} processing")
				yield page
		finally:
			task.cancel()
			try:
				await asyncio.wait_for(task, timeout=5.0)
			except (asyncio.CancelledError, asyncio.TimeoutError):
				pass

			print(f"Success: {len(self._successful_urls)} Failed: {len(self._failed_urls)}")

	async def get_books_async(self) -> AsyncGenerator[Book, None]:
		async def producer():
			tasks = []
			async for page_text in self.get_page_async():
				task = asyncio.create_task(self.parse_books(page_text))
				tasks.append(task)
			await asyncio.gather(*tasks)
			await self.queueBooks.put(self._stop_marker)

		task = asyncio.create_task(producer())
		c = 0
		try:
			while True:
				try:
					book = await asyncio.wait_for(self.queueBooks.get(), timeout=60.0)
				except asyncio.TimeoutError:
					print("Timeout waiting for book")
					break

				if book is self._stop_marker:
					print(f"Total books: {c}")
					break

				c += 1
				yield book
		finally:
			task.cancel()
			try:
				await asyncio.wait_for(task, timeout=5.0)
			except (asyncio.CancelledError, asyncio.TimeoutError):
				pass
