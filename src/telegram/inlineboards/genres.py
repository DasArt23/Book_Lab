import math
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ALL_GENRES = [
    "Travel", "Mystery", "Historical Fiction", "Sequential Art", "Classics",
    "Philosophy", "Romance", "Womens Fiction", "Fiction", "Childrens",
    "Religion", "Nonfiction", "Music", "Science Fiction", "Sports and Games",
    "Fantasy", "Young Adult", "Science", "Poetry", "History"
]

# Сопоставление названий жанров с URL
GENRE_URLS = {
    "travel": "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
    "mystery": "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
    "historical_fiction": "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html",
    "sequential_art": "https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html",
    "classics": "https://books.toscrape.com/catalogue/category/books/classics_6/index.html",
    "philosophy": "https://books.toscrape.com/catalogue/category/books/philosophy_7/index.html",
    "romance": "https://books.toscrape.com/catalogue/category/books/romance_8/index.html",
    "womens_fiction": "https://books.toscrape.com/catalogue/category/books/womens-fiction_9/index.html",
    "fiction": "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html",
    "childrens": "https://books.toscrape.com/catalogue/category/books/childrens_11/index.html",
    "religion": "https://books.toscrape.com/catalogue/category/books/religion_12/index.html",
    "nonfiction": "https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html",
    "music": "https://books.toscrape.com/catalogue/category/books/music_14/index.html",
    "science_fiction": "https://books.toscrape.com/catalogue/category/books/science-fiction_15/index.html",
    "sports_and_games": "https://books.toscrape.com/catalogue/category/books/sports-and-games_16/index.html",
    "fantasy": "https://books.toscrape.com/catalogue/category/books/fantasy_17/index.html",
    "young_adult": "https://books.toscrape.com/catalogue/category/books/young-adult_18/index.html",
    "science": "https://books.toscrape.com/catalogue/category/books/science_19/index.html",
    "poetry": "https://books.toscrape.com/catalogue/category/books/poetry_20/index.html",
    "history": "https://books.toscrape.com/catalogue/category/books/history_21/index.html",
}

ITEMS_PER_PAGE = 6


def get_genres_keyboard(page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_genres = ALL_GENRES[start_idx:end_idx]

    for genre in page_genres:
        # Преобразуем название жанра в slug для callback_data
        slug = genre.lower().replace(' ', '_').replace('-', '_')
        builder.button(text=genre, callback_data=f"genre_{slug}")

    builder.adjust(2)  # Жанры по 2 в ряд

    nav_buttons = []
    total_pages = math.ceil(len(ALL_GENRES) / ITEMS_PER_PAGE)

    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="◀ Назад", callback_data=f"page_{page - 1}"))

    nav_buttons.append(InlineKeyboardButton(text=f"{page + 1}/{total_pages}", callback_data="noop"))

    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton(text="Вперед ▶", callback_data=f"page_{page + 1}"))

    builder.row(*nav_buttons)
    return builder.as_markup()


def get_genre_url(genre_slug: str) -> str:
    """Возвращает URL для выбранного жанра"""
    return GENRE_URLS.get(genre_slug)
