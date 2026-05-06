from .engine import Books_handler, ID_handler, Year_handler, Text_handler
from .source import Books_source, Rand_source, Demo_source, FileJSON_source

class Sources_factory:
    _sources = {
        "rand": Rand_source,
        "json": FileJSON_source,
        "demo": Demo_source,
    }

    @classmethod
    def get_source(cls, source_type: str, **kwargs) -> Books_source:
        """Создает и возвращает источник данных """
        source = cls._sources.get(source_type)

        if not source:
            raise ValueError(f"Неизвестный тип источник: {source_type}")

        return source(**kwargs)

class Handler_factory:
    _handlers = {
        "text": Text_handler,
        "id": ID_handler,
        "year": Year_handler,
    }

    @classmethod
    def get_handler(cls, handler_type: str, **kwargs) -> Books_handler:
        """Создает и возвращает источник данных """
        handler = cls._handlers.get(handler_type)

        if not handler:
            raise ValueError(f"Неизвестный тип обработчика: {handler_type}")

        return handler(**kwargs)


