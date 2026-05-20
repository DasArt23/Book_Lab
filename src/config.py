from enum import Enum
from data_processing.parser import Demo_parser
import argparse


class ExecutionMode(Enum):
    """Режимы выполнения обработки"""
    SEQUENTIAL = "sequential"
    THREAD = "thread"
    PROCESS = "process"
    ASYNC = "async"


class AppConfig():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance._set_up()
        return cls._instance

    def _set_up(self):
        """Хранение данных программы"""
        self.handler_type = "text"
        self.handler_param = {
            "rec_id": 505,
            "treshold": 3,
        }

        self.sources_list = [
            {"source_type": "json", "path": "json_files/proba.json"},
            {"source_type": "demo"},
            {"source_type": "rand", "amount": 6},
            #{"source_type": "rand", "amount": 1000},
            {"source_type": "parse", "urls": [
                "https://books.toscrape.com/catalogue/category/books_1/index.html",
                "https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-2.html",
            ]},
            {"source_type": "parse", "urls": [
                "https://books.toscrape.com/catalogue/category/books_1/index.html",
            ]}
        ]

        self.parsers = [
            Demo_parser("json_files/demo1.json"),
            Demo_parser("json_files/demo2.json", genre="fiction_10"),
            Demo_parser("json_files/demo3.json", page="page-3")
        ]

        self.app_version = "v1.5.1"
        self.debug = True

        self.execution_mode = ExecutionMode.SEQUENTIAL
        self._max_workers = 4

        self._parse_arguments()

        self.max_concurrent_requests = 3
        self.request_delay = 1.0
        self.retry_count = 3
        self.retry_backoff_factor = 2.0
        self.request_timeout = 10.0
        self.rate_limit_cooldown = 60.0

    def get_data_from_parsing(self) -> None:
        """
            Получает данные из парсеров и создает источника
            для обработки последовательно
        """
        for parser in self.parsers:
            parser.parse_books()
            self.sources_list.append({
                "source_type": parser.file_type,
                "path": parser.filename,
            })

    def get_sources(self):
        """Получение данных для обработки"""
        yield from self.sources_list

    def _parse_arguments(self):
        parser = argparse.ArgumentParser(
            description=f"Приложение для обработки данных v{self.app_version}",
            formatter_class=argparse.RawTextHelpFormatter
        )

        parser.add_argument(
            "-m", "--mode",
            type=str,
            choices=[mode.value for mode in ExecutionMode],
            default=self.execution_mode.value,
            help=f"""Режим выполнения обработки:
            sequential - последовательный режим (по умолчанию)
            thread     - многопоточный режим
            process    - многопроцессный режим
            async      - асинхронный режим
            """
        )

        parser.add_argument(
            "-w", "--workers",
            type=int,
            default=self.max_workers,
            help=f"Количество потоков/процессов"\
                  "(по умолчанию: {self.max_workers})"
        )

        args = parser.parse_args()

        self.workers = args.workers
        self.execution_mode = ExecutionMode(args.mode)

    @property
    def max_workers(self):
        return self._max_workers

    @max_workers.setter
    def max_workers(self, value):
        if value >= 2:
            self._max_workers = value

    @property
    def is_async_mode(self) -> bool:
        """Проверка, запущен ли асинхронный режим"""
        return self.execution_mode == ExecutionMode.ASYNC
