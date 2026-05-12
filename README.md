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
Можно указать параметры MODE и W

## Вывод программы после запуска проекта
```
Получено данных: 3

Изменения:
  Year: 9647 -> 2026
  Metadata: {'source': 'JSON source', 'category': 'Text', 'tags': []} -> {'source': 'JSON source', 'category': 'Text', 'tags': [], 'modern': True}
Количество изменений: 1
Получено данных: 2

Изменения:
  Year: 20012 -> 2026
  Metadata: {'source': 'Demo source', 'category': 'Text', 'tags': []} -> {'source': 'Demo source', 'category': 'Text', 'tags': [], 'modern': True}
Количество изменений: 1
Получено данных: 6

Изменения:
  Year: 2374 -> 2026
  Metadata: {'source': 'Random source', 'category': 'Text', 'tags': []} -> {'source': 'Random source', 'category': 'Text', 'tags': [], 'modern': True}

Изменения:
  Year: 2332 -> 2026
  Metadata: {'source': 'Random source', 'category': 'Text', 'tags': []} -> {'source': 'Random source', 'category': 'Text', 'tags': [], 'modern': True}

Изменения:
  Year: 2719 -> 2026
  Metadata: {'source': 'Random source', 'category': 'Text', 'tags': []} -> {'source': 'Random source', 'category': 'Text', 'tags': [], 'modern': True}
Количество изменений: 3
Получено из источника JSON source: 3
Изменено данных источника JSON source: 1

Получено из источника Demo source: 2
Изменено данных источника Demo source: 1

Получено из источника Random source: 6
Изменено данных источника Random source: 3

Время выполнения: 6.228 секунд
Программа завершилась успешно
```
Можно добавить различные источники данных или изменить обработчик, модифицируя класс **AppConfig**.
При добавлении источника **FikeJSON_source** указывайте путь *"json_file/ваш_json_файл"*. Json файл должен иметь вид:
```
{
	"Book1":{
		"recorder_id": 1231451,
		"author": "Jord Clone",
		"favourite": 1
	},
	" python":{
		"recorder_id": 8737
	},
	"Идиот":{
		"recorder_id": 856395,
		"author": "Федор Достоевский",
		"year": 1235
	}
}
```

### Структура проекта
```
project_Bakin_505
├── Makefile
├── pyproject.toml
├── README.md
├── src
│   ├── application.py
│   ├── config.py
│   ├── core
│   │   ├── mode_manager.py
│   │   └── timer.py
│   ├── data_processing
│   │   ├── engine.py
│   │   ├── fabrics.py
│   │   ├── json_files
│   │   │   ├── demo1.json
│   │   │   ├── demo2.json
│   │   │   ├── demo3.json
│   │   │   ├── good.json
│   │   │   └── proba.json
│   │   ├── parser.py
│   │   └── source.py
│   ├── domain
│   │   ├── constants.py
│   │   ├── models.py
│   │   └── work_unit.py
│   └── main.py
└── uv.lock
```
### Makefile
```
MODE ?= sequential
W ?= 4

install:
	uv sync
build:
	uv build
project:
	uv run start -m $(MODE) -w $(W)
lint:
	uv tool run ruff check
```
Где при запуске можно назначить: 
- MODE = sequential,thread,process для выбора режима обработки
- W = количество потоков
