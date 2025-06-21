# bot/set_commands.py

from aiogram.types import BotCommand, BotCommandScopeChat
from aiogram import Bot
from bot.config import ADMIN_ID

async def set_admin_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Botni ishga tushirish"),
        BotCommand(command="/admin", description="Admin panel"),
        BotCommand(command="/mycourses", description="Mening kurslarim"),
        BotCommand(command="/help", description="Yordam"),
        BotCommand(command="/check_users", description="📋 Barcha kursdagi foydalanuvchilar"),
        BotCommand(command="/pay_123456789", description="💳 To‘lov holatini belgilash"),
    ]

    # Faqat admin uchun komandalarni o‘rnatamiz
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeChat(chat_id=ADMIN_ID)
    )
