from aiogram import Router, F
from aiogram.types import Message
from telegram.keyboards.menu import add_sources
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from telegram.states import EnterNum, EnterPath
from config import AppConfig

router = Router()


@router.message(EnterNum.ch_num, F.text.strip().isdigit())
async def set_num(message: Message, state: FSMContext):
    num = await state.get_data()
    AppConfig().add_source({"source_type": "rand", "amount": max(num, 1)})
    await message.answer(
        "Хотите добавить еще источник?",
        reply_markup=add_sources(),
    )


@router.message(EnterNum.ch_num, F.text)
async def not_num(message: Message, state: FSMContext):
    AppConfig().add_source({"source_type": "rand", "amount": 6})
    await message.answer(
        "Это не число.\nХотите добавить еще источник?",
        reply_markup=add_sources(),
    )

@router.message(EnterPath.ch_path, F.text.strip().endswith('.json'))
async def set_path(message: Message, state: FSMContext):
    clean_path = message.text.strip()
    AppConfig().add_source({"source_type": "json", "path": clean_path})
    await state.update_data(json_path=clean_path)
    await message.answer(
        "Хотите добавить еще источник?",
        reply_markup=add_sources(),
    )

@router.message(EnterPath.ch_path, F.text)
async def not_path(message: Message, state: FSMContext):
    DEFAULT_PATH = "json_files/proba.json"
    AppConfig().add_source({"source_type": "json", "path": "json_files/proba.json"})
    await state.update_data(json_path=DEFAULT_PATH)
    await message.answer(
        "Это не путь к json файлу.\nХотите добавить еще источник?",
        reply_markup=add_sources(),
    )

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
async def get_json_path(message: Message, state: FSMContext):
    await message.answer("Выберите, что хотите добавить")
    await state.set_state(EnterPath.ch_path)
