from aiogram import Router, F
from aiogram.types import Message
from telegram.keyboards.menu import add_sources
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from telegram.states import EnterNum
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
