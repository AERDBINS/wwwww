import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.config import BOT_TOKEN
from bot.handlers import routers  # barcha routerlar shu ro‘yxatda bo‘ladi
from bot.set_commands import set_admin_commands


async def main():
    print("✅ Bot ishga tushmoqda...")

    # Bot va Dispatcher obyektlari
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Routerlarni ulash
    for router in routers:
        dp.include_router(router)

    # Admin komandalarni o‘rnatish
    await set_admin_commands(bot)

    # Polling orqali ishga tushirish
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
