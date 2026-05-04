
class AppConfig():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            cls._instance._set_up()
        return cls._instance

    def _set_up(self):
        """Хранение данных программы"""
        self.handler_type = "year"
        self.handler_param = {
            "rec_id": 505,
            "treshold": 3,
        }

        self.sources_list = [
            {"source_type": "json", "path": "json_files/proba.json"},
            {"source_type": "demo"},
            {"source_type": "rand", "amount": 6},
            {"source_type": "rand", "amount": 100000}
        ]

        self.app_version = "v1.5.1"
        self.debug = True

    def get_sources(self):
        """Получение данных для обработки"""
        yield from self.sources_list
