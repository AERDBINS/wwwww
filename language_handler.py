from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards import main_menu_keyboard

router = Router()

@router.message(F.text.in_(["🇺🇿 O‘zbek tili", "🇷🇺 Русский язык", "🇬🇧 English"]))
async def set_language(message: Message):
    lang_map = {
        "🇺🇿 O‘zbek tili": "uz",
        "🇷🇺 Русский язык": "ru",
        "🇬🇧 English": "en"
    }

    lang = lang_map.get(message.text, "uz")
    await message.answer("🏠 Asosiy menyu:", reply_markup=main_menu_keyboard(lang))
