import os
from aiogram import Bot, Dispatcher
from domain.constants import TOKEN
import telegram.handlers.commands as commands
import telegram.handlers.parsing as parsing
from aiohttp import web


async def handle(request):
    return web.Response(text="Bot is alive")


async def start_fake_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.session.close()


async def run_bot():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(commands.router, parsing.router)

    dp.shutdown.register(on_shutdown)

    # Запускаем веб-сервер, чтобы Render одобрил деплой
    await start_fake_server()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, polling_timeout=10)
