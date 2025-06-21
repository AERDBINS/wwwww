from aiogram import Bot
from aiogram.types import User
from bot.config import CHANNEL_USERNAME

async def check_user_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return member.status in ("member", "creator", "administrator")
    except Exception:
        return False
