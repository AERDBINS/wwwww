from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards import main_menu_keyboard
from bot.keyboards import subscribe_keyboard, language_keyboard
from bot.utils.check_subscription import check_user_subscription
from aiogram.types import CallbackQuery

router = Router()

@router.message(F.text.in_(["🇺🇿 O‘zbek tili", "🇷🇺 Русский язык", "🇬🇧 English"]))
async def set_language(message: Message):
    lang_map = {
        "🇺🇿 O‘zbek tili": "uz",
        "🇷🇺 Русский язык": "ru",
        "🇬🇧 English": "en"
    }

    lang = lang_map.get(message.text, "uz")  # Default fallback

    await message.answer("🏠 Asosiy menyu:", reply_markup=main_menu_keyboard(lang))

@router.message(F.text == "/start")
async def start_handler(message: Message, bot):
    user_id = message.from_user.id
    is_member = await check_user_subscription(bot, user_id)

    if not is_member:
        await message.answer("⚠️ Avval kanalga obuna bo‘ling:", reply_markup=subscribe_keyboard())
        return

    await message.answer("🇺🇿 Iltimos, tilni tanlang:", reply_markup=language_keyboard())

@router.callback_query(F.data == "check_subscription")
async def check_sub(call: CallbackQuery, bot):
    user_id = call.from_user.id
    if await check_user_subscription(bot, user_id):
        await call.message.answer("✅ Obuna tasdiqlandi. Tilni tanlang:", reply_markup=language_keyboard())
        await call.message.delete()  # eski inline tugmani o‘chirish uchun

    else:
        await call.answer("🚫 Obuna topilmadi", show_alert=True)
