from domain.models import Book
from data_processing.engine import Books_handler
from typing import Tuple


class BookWorkUnit:
    def __init__(self, handler: Books_handler):
        self.handler = handler

    def __call__(self, book: Book) -> Tuple[Book, Book]:
        """Обработка данных с помощью обработчика"""
        # import time
        # time.sleep(0.1) #Для искусственной проверки того, что thread и process быстрее последовательной
        try:
            processed_book = self.handler.handler_book(book)
            return book, processed_book
        except Exception:
            return book, book

    def __reduce__(self):
        """Для корректной сериализации данных"""
        return (self.__class__, (self.handler,))

