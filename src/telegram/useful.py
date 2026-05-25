import asyncio
import inspect
import main
import json


def book_to_dict(book) -> dict:
    return {attr: getattr(book, attr) for attr in vars(book).keys()}


async def execute_main_and_build_json(user_id: int) -> str:
    # Запускаем main() в executor, так как внутри могут быть синхронные тяжелые вызовы
    loop = asyncio.get_running_loop()
    app = await loop.run_in_executor(None, main)

    processed_books = []

    # Проверяем, какой генератор вернулся в result
    if inspect.isasyncgen(app.result):
        async for book in app.result:
            processed_books.append(book_to_dict(book))
    else:
        # Если генератор синхронный, выгребаем его в executor
        def consume_sync():
            return [book_to_dict(book) for book in app.result]
        processed_books = await loop.run_in_executor(None, consume_sync)

    file_path = f"books_result_{user_id}.json"

    def save_json():
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(processed_books, f, ensure_ascii=False, indent=4)

    await loop.run_in_executor(None, save_json)
    return file_path
