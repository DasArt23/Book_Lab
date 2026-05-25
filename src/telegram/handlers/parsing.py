from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from telegram.keyboards.menu import add_sources, get_handlers_menu, get_modes_menu, get_start_menu
from telegram.inlineboards.genres import get_genres_keyboard
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from telegram.states import EnterNum, EnterPath, EnterHandler
from config import AppConfig
from telegram.useful import execute_main_and_build_json
import os

router = Router()


@router.message(StateFilter(EnterNum.ch_num))
async def handle_rand_amount(message: Message, state: FSMContext):
    text = message.text.strip()

    if text.isdigit():
        amount = int(text)
        AppConfig().add_source({"source_type": "rand", "amount": max(amount, 1)})
        await message.answer(
            f"✅ Добавлен источник с {amount} книгами.\nХотите добавить еще?",
            reply_markup=add_sources(),
        )
    else:
        AppConfig().add_source({"source_type": "rand", "amount": 6})
        await message.answer(
            "❌ Это не число. Добавлен источник с 6 книгами.\nХотите добавить еще?",
            reply_markup=add_sources(),
        )

    await state.clear()


@router.message(EnterPath.ch_path, F.text.strip().endswith('.json'))
async def set_path(message: Message, state: FSMContext):
    clean_path = message.text.strip()
    AppConfig().add_source({"source_type": "json", "path": clean_path})
    await message.answer(
        "Хотите добавить еще источник?",
        reply_markup=add_sources(),
    )
    await state.clear()


@router.message(EnterPath.ch_path, F.text)
async def not_path(message: Message, state: FSMContext):
    DEFAULT_PATH = "json_files/proba.json"
    AppConfig().add_source({"source_type": "json", "path": "json_files/proba.json"})
    await message.answer(
        "Это не путь к json файлу.\nХотите добавить еще источник?",
        reply_markup=add_sources(),
    )
    await state.clear()


@router.message(F.text.lower() == "получить книги")
async def set_sources(message: Message):
    await message.answer(
        "Выберите источник, откуда хотите получить книги",
        reply_markup=add_sources(),
    )


@router.message(StateFilter(None), F.text.lower() == "rand")
async def get_rand_num(message: Message, state: FSMContext):
    await message.answer("Введите число случайных элементов")
    await state.set_state(EnterNum.ch_num)


@router.message(StateFilter(None), F.text.lower() == "json")
async def get_json_path(message: Message, state: FSMContext):
    await message.answer("Введите путь до json файла")
    await state.set_state(EnterPath.ch_path)


@router.message(StateFilter(None), F.text.lower() == "demo")
async def set_demo_source(message: Message):
    AppConfig().add_source({"source_type": "demo"})
    await message.answer(
        "Демо-источник успешно добавлен!\nХотите добавить еще источник?",
        reply_markup=add_sources(),
    )


@router.message(StateFilter(None), F.text.lower() == "parse")
async def show_genres(message: Message):
    await message.answer(
        text="Выберите жанр для парсинга:",
        reply_markup=get_genres_keyboard(page=0)
    )


@router.message(EnterHandler.ch_type, F.text.lower().endswith("_handler"))
async def handle_handler_selection(message: Message, state: FSMContext):
    handler_text = message.text.lower()

    if handler_text == "text_handler":
        AppConfig().set_handler(
            handler_type="text",
            rec_id=505,
            threshold=3
        )
        await message.answer(
            text="✅ Выбран Text_handler\n\nВыберите режим запуска:",
            reply_markup=get_modes_menu()
        )
        await state.set_state(EnterHandler.ch_mode)

    elif handler_text == "id_handler":
        await message.answer(
            text="Введите ID записи (rec_id):\n(по умолчанию: 505)"
        )
        await state.set_state(EnterHandler.ch_rec_id)
        await state.update_data(h_type="id")

    elif handler_text == "year_handler":
        await message.answer(
            text="Введите порог года (threshold):\n(по умолчанию: 3)"
        )
        await state.set_state(EnterHandler.ch_threshold)
        await state.update_data(h_type="year")


@router.callback_query(F.data.startswith("page_"))
async def process_page_change(callback: CallbackQuery):
    page = int(callback.data.split("_")[1])

    await callback.message.edit_reply_markup(
        reply_markup=get_genres_keyboard(page=page)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("genre_"))
async def process_genre_select(callback: CallbackQuery):
    genre_name = callback.data.split("_")[1]

    # Добавление логики конфигурации
    AppConfig().add_source({"source_type": "parse", "genre": genre_name})
    await callback.message.answer(
        text=f"Жанр «{genre_name.capitalize()}» успешно добавлен как источник!\nХотите добавить еще?",
        reply_markup=add_sources() # Ваша Reply-клавиатура управления
    )
    await callback.answer()


@router.message(StateFilter(None), F.text.lower() == "просмотреть")
async def view_config(message: Message):
    current_sources = AppConfig().get_sources()

    if not current_sources:
        await message.answer("Список источников пуст.")
        return

    lines = []
    for idx, src in enumerate(current_sources, 1):
        st = src.get("source_type")
        if st == "rand":
            lines.append(f"{idx}. Random ({src.get('amount', 1)} шт.)")
        elif st == "json":
            lines.append(f"{idx}. JSON ({src.get('path')})")
        elif st == "parse":
            lines.append(f"{idx}. Parse ({src.get('genre', 'all')})")
        elif st == "demo":
            lines.append(f"{idx}. Demo")

    await message.answer("📋 Источники:\n" + "\n".join(lines))


@router.message(StateFilter(None), F.text.lower() == "очистить")
async def clear_config(message: Message):
    AppConfig().reset_sources()
    await message.answer("🗑 Источники очищены.")


@router.message(F.text.lower() == "хватит")
async def finish_config(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Нужно выбрать обработчика:",
        reply_markup=get_handlers_menu()
    )
    await state.set_state(EnterHandler.ch_type)


@router.message(EnterHandler.ch_mode, F.text.in_({"sequential", "thread", "process", "async"}))
async def set_program_mode(message: Message, state: FSMContext):
    AppConfig().change_mode(message.text)
    await state.clear()

    status_msg = await message.answer("Запуск обработки и сборка JSON...")

    try:
        json_file_path = await execute_main_and_build_json(message.from_user.id)

        document = FSInputFile(json_file_path)
        await message.answer_document(
            document=document,
            caption="Книги успешно обработаны через генератор в main()!"
        )
        await status_msg.delete()

        if os.path.exists(json_file_path):
            os.remove(json_file_path)
    except Exception as e:
        await message.answer(f"Ошибка выполнения: {str(e)}")

    await message.answer("Что делаем дальше?", reply_markup=get_start_menu())


@router.message(EnterHandler.ch_rec_id)
async def set_rec_id(message: Message, state: FSMContext):
    val = message.text.strip()
    rec_id = int(val) if val.isdigit() else 505
    data = await state.get_data()

    AppConfig().set_handler(handler_type=data["h_type"], rec_id=rec_id, threshold=3)
    await message.answer(text="Выберите режим запуска программы:", reply_markup=get_modes_menu())
    await state.set_state(EnterHandler.ch_mode)


@router.message(EnterHandler.ch_threshold)
async def set_threshold(message: Message, state: FSMContext):
    val = message.text.strip()
    threshold_val = int(val) if val.isdigit() else 3
    data = await state.get_data()

    AppConfig().set_handler(handler_type=data["h_type"], rec_id=505, threshold=threshold_val)
    await message.answer(text="Выберите режим запуска программы:", reply_markup=get_modes_menu())
    await state.set_state(EnterHandler.ch_mode)


@router.message(EnterHandler.ch_mode)
async def invalid_program_mode(message: Message):
    await message.answer(
        text="Пожалуйста, выберите режим из меню:",
        reply_markup=get_modes_menu()
    )
