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
Получено данных: 3

Изменения:
_Title:  python -> Python
_Author:  -> Unknown

Больше изменений нет
Количетсов изменений: 1
Получено данных: 2

Изменения:
_Title: The War   of the Worlds -> The War Of The Worlds

Изменения:
_Author: А.П. чехов -> А.П. Чехов

Больше изменений нет
Количетсов изменений: 2
Получено данных: 6

Изменения:
_Title: purple slipper -> Purple Slipper
_Author: S. q. high -> S. Q. High

Изменения:
_Title: barbarous hardship -> Barbarous Hardship
_Author: Y. m. joy -> Y. M. Joy

Изменения:
_Title: quizzical strength -> Quizzical Strength
_Author: c. K. radiator -> C. K. Radiator

Изменения:
_Title: unequaled paint -> Unequaled Paint
_Author: f. v. node -> F. V. Node

Изменения:
_Title: magical cop-out -> Magical Cop-Out
_Author: E. E. bush -> E. E. Bush

Изменения:
_Title: icky stot -> Icky Stot
_Author: V. C. epic -> V. C. Epic

Больше изменений нет
Количетсов изменений: 6
Получено из источника JSON source: 3
Изменено данных источника JSON source: 1

Получено из источника Demo source: 2
Изменено данных источника Demo source: 2

Получено из источника Random source: 6
Изменено данных источника Random source: 6

Программа завершилась успешно
```
Также в модуле main можно добавить различные источники данных.
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
		"author": "Федор Достоевский"
	}
}
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
│   │   ├── json_files
│   │   │   ├── good.json
│   │   │   └── proba.json
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