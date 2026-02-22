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
Получено данных: 2

Изменения:
Title: The War   of the Worlds -> The War Of The Worlds

Изменения:
Title:   Вишневый сад -> Вишневый Сад
Author: А.П. чехов -> А.П. Чехов

Больше изменений нет
Количетсов изменений: 2
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