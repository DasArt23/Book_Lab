import math
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

ALL_GENRES = [
    "Travel", "Mystery", "Historical Fiction", "Sequential Art", "Classics",
    "Philosophy", "Romance", "Womens Fiction", "Fiction", "Childrens",
    "Religion", "Nonfiction", "Music", "Science Fiction", "Sports and Games",
    "Fantasy", "Young Adult", "Science", "Poetry", "History"
]


ITEMS_PER_PAGE = 6

def get_genres_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_genres = ALL_GENRES[start_idx:end_idx]

    for genre in page_genres:
        builder.button(text=genre, callback_data=f"genre_{genre.lower().replace(' ', '_')}")
    builder.adjust(2) # Жанры по 2 в ряд

    nav_buttons = []
    total_pages = math.ceil(len(ALL_GENRES) / ITEMS_PER_PAGE)

    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="<<", callback_data=f"page_{page - 1}"))

    nav_buttons.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="noop"))

    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text=">>", callback_data=f"page_{page + 1}"))

    builder.row(*nav_buttons)
    return builder.as_markup()
