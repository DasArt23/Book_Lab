from aiogram import Bot, Dispatcher
from domain.constants import TOKEN
import telegram.handlers.commands as commands


async def run_bot():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(commands.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
