from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from domain.constants import TOKEN
import telegram.handlers.commands as commands


async def run_bot():
    print("Запуск бота пошел")
    session = AiohttpSession(proxy='http://195.201.141.139:80')

    bot = Bot(token=TOKEN, session=session)
    dp = Dispatcher()
    dp.include_routers(commands.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
