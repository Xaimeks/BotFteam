import asyncio
import logging
import sys
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import cmd_start, profile_handler, payments_handler, admin, settings_handler, main_menu, admin_contact

async def main() -> None:
    load_dotenv()
    TOKEN = getenv("BOT_TOKEN")

    dp = Dispatcher()
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp.include_routers(
        cmd_start.router, profile_handler.router, payments_handler.router, admin.router, settings_handler.router, main_menu.router, admin_contact.router
        )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())