from domain.models import Book
from data_processing.engine import Books_handler
from typing import Tuple
import asyncio

class BookWorkUnit:
    def __init__(self, handler: Books_handler):
        self.handler = handler

    def __call__(self, book: Book) -> Tuple[Book, Book]:
        """Обработка данных с помощью обработчика"""
        # import time
        # time.sleep(0.1)
        try:
            processed_book = self.handler.handler_book(book)
            return book, processed_book
        except Exception:
            return book, book

    async def __call_async__(self, book: Book) -> Tuple[Book, Book]:
        """Асинхронный вызов"""
        await asyncio.sleep(0.01)  # имитация I/O
        try:
            processed_book = self.handler.handler_book(book)
            return book, processed_book
        except Exception:
            return book, book

    def __reduce__(self):
        """Для корректной сериализации данных"""
        return (self.__class__, (self.handler,))

