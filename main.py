import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)

from app.config import (
    BOT_TOKEN,
    PORT,
    RUN_MODE,
    WEBHOOK_BASE_URL,
    WEBHOOK_SECRET,
)
from app.handlers import router

WEBHOOK_PATH = "/telegram/webhook"


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_router(router)
    return dispatcher


async def run_polling():
    bot = Bot(token=BOT_TOKEN)
    dispatcher = create_dispatcher()

    try:
        # Polling працює лише тоді, коли webhook вимкнений.
        await bot.delete_webhook(drop_pending_updates=False)
        await dispatcher.start_polling(
            bot,
            close_bot_session=False,
        )
    finally:
        await bot.session.close()


async def health(request: web.Request):
    return web.Response(text="Bot is running")


def run_webhook():
    if not WEBHOOK_BASE_URL.startswith("https://"):
        raise RuntimeError(
            "Для webhook задай WEBHOOK_BASE_URL з https://"
        )

    if not WEBHOOK_SECRET:
        raise RuntimeError("Задай WEBHOOK_SECRET")

    bot = Bot(token=BOT_TOKEN)
    dispatcher = create_dispatcher()

    async def on_startup(bot: Bot):
        await bot.set_webhook(
            url=f"{WEBHOOK_BASE_URL}{WEBHOOK_PATH}",
            secret_token=WEBHOOK_SECRET,
            allowed_updates=dispatcher.resolve_used_update_types(),
        )

    dispatcher.startup.register(on_startup)

    application = web.Application()
    application.router.add_get("/", health)

    SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
        handle_in_background=True,
    ).register(
        application,
        path=WEBHOOK_PATH,
    )

    setup_application(application, dispatcher, bot=bot)

    web.run_app(
        application,
        host="0.0.0.0",
        port=PORT,
        access_log=None,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if RUN_MODE == "polling":
        asyncio.run(run_polling())
    elif RUN_MODE == "webhook":
        run_webhook()
    else:
        raise RuntimeError("RUN_MODE має бути polling або webhook")