from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode

router = Router()


@router.message(Command('start'))
async def bot_start(message: Message):
    await message.answer(
        f"Здравствуйте, <b>{message.from_user.full_name}</b>!",
        parse_mode=ParseMode.HTML,
    )
