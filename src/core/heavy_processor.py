import hashlib
from domain.models import Book
from typing import Tuple


class HeavyProcessor:
    @staticmethod
    def process_book(book: Book, handler) -> Tuple[Book, Book]:
        """
        Тяжелая обработка одной книги.
        Может выполняться в отдельном потоке или процессе.
        """
        # Симуляция тяжелых вычислений
        for i in range(10000):
            _ = i * i
        
        # Хеширование для нагрузки
        text = f"{book.title}{book.author}{book.year}"
        for i in range(100):
            text = hashlib.md5(text.encode()).hexdigest()
        
        processed = handler.handler_book(book)
        return book, processed
    
    @staticmethod
    def process_books(books: list, handler) -> list:
        results = []
        for book in books:
            results.append(HeavyProcessor.process_book(book, handler))
        return results
