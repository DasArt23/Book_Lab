from bs4 import BeautifulSoup, PageElement
from abc import ABC, abstractmethod
from domain.models import Book
from fake_useragent import UserAgent
from pathlib import Path
import json
import requests

class Parser(ABC):
    _name = "parser"
    _file_type = "json"

    @property
    @abstractmethod
    def filename(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def file_type(self):
        return self._file_type

    def save_results(self, data) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_page(self) -> str:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        page = requests.get(self.url, headers=headers, timeout=10)
        if page.status_code == 200:
            return page.text
        print(f"Страница не получена по адресу {self.url}")
        return ""

    @staticmethod
    def get_book(book_element: PageElement) -> tuple[str, dict]:
        pass

    @abstractmethod
    def parse_books(self) -> None:
        pass

class Demo_parser(Parser):
    _name = "Book to scrape parser"

    def __init__(self, file_path: str, **params):
        """в params могут сожержаться genre и page"""
        self._filename = file_path
        self.file_path = (Path(__file__).parent / file_path).resolve()
        p = params.get('genre', '')
        self.url = f"https://books.toscrape.com/catalogue/category/{f'books/{p}' if p else 'books_1'}/{params.get('page', 'index')}.html"

    @property
    def filename(self):
        return self._filename

    @staticmethod
    def get_book(book_element: PageElement):
        data = book_element.findAll('a')[1]
        title = data['title']
        url = data['href']
        data = {
            'url': url,
        }
        return (title, data)

    def parse_books(self) -> None:
        print(f"Получение данных из парсинга: {self.name}")
        page = self.get_page()
        if not page:
            return
        soup = BeautifulSoup(page, "html.parser")
        books = soup.findAll("li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"})
        books_data = dict()
        for book in books:
            title, data = self.get_book(book)
            books_data[title] = data
        self.save_results(books_data)
