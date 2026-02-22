# Программа поиска книг

## Установка

### Установка пакетного менеджера uv
Инструкция по установке uv находится по ссылке https://docs.astral.sh/uv/getting-started/installation/

### С помощью git
1. git clone git@gitlab.digital.mephi.ru:dasart/project_Bakin_505
2. cd project_Bakin_505
3. make build

## Использование
Программа запускается при запуске команды **make project**

## Вывод программы после запуска проекта
```
Title: The War of the Worlds   | Author: H.G. Wells
ID: 123
Meta: source=Test, category=Audio, tags=[]
Title: The War Of The Worlds | Author: H.G. Wells
ID: 123
Meta: source=Test, category=Audio, tags=[]
Книги не одинаковы

Больше изменений нет
Программа завершилась успешно
```

### Структура проекта
```
project_Bakin_505
├── Makefile
├── README.md
├── pyproject.toml
├── src
│   ├── application.py
│   ├── data_processing
│   │   ├── engine.py
│   │   └── source.py
│   ├── domain
│   │   └── models.py
│   └── main.py
└── uv.lock
```
### Makefile
```
install:
		uv sync
build:
		uv build
project:
		uv run start
lint:
		uv tool run ruff check
```