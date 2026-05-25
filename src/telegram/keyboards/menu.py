from aiogram.types import KeyboardButton, ReplyHeyboardMarkup
from data_processing.fabrics import Sources_factory
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_start_menu():
    buttons = [
            KeyboardButton(text="Получить книги"),
    ]
    return ReplyHeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Добавьте источники книг"
    )


def add_sources():
    builder = ReplyKeyboardBuilder()
    names = Sources_factory._sources.keys()
    for source_name in names:
        builder.add(KeyboardButton(text=source_name))
    builder.adjust(2)
    builder.add(KeyboardButton(text="Хватит"))
    builder.add(KeyboardButton(text="Очистить"))
    builder.add(KeyboardButton(text="Просмотреть список источников"))
    return builder.as_markup(resize_keyboard=True)
