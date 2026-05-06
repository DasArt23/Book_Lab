from data_processing.parser import Demo_parser, Parser

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
            #{"source_type": "rand", "amount": 100000}
        ]

        self.parsers = [
            Demo_parser("json_files/demo1.json"),
            Demo_parser("json_files/demo2.json", genre="fiction_10"),
            Demo_parser("json_files/demo3.json", page="page-3")
        ]

        self.app_version = "v1.5.1"
        self.debug = True

    def get_data_from_parsing(self) -> None:
        """Получает данные из парсеров и создает источника для обработки"""
        for parser in self.parsers:
            parser.parse_books()
            self.sources_list.append({
                "source_type": parser.file_type,
                "path": parser.filename,
            })

    def get_sources(self):
        """Получение данных для обработки"""
        self.get_data_from_parsing()
        yield from self.sources_list
