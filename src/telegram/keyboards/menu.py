from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from data_processing.fabrics import Sources_factory
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_start_menu():
    buttons = [
            [KeyboardButton(text="Получить книги")],
    ]
    return ReplyKeyboardMarkup(
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
    builder.row(KeyboardButton(text="Хватит"))
    builder.row(KeyboardButton(text="Очистить"))
    builder.row(KeyboardButton(text="Просмотреть"))
    return builder.as_markup(resize_keyboard=True)
