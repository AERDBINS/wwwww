from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards import main_menu_keyboard
from bot.user_data import is_registered, get_user_data
from bot.config import ADMIN_ID

import json
from pathlib import Path

router = Router()

# Fayl joyi (kursga yozilganlar uchun)
ENROLLMENT_FILE = Path("data/enrollments.json")


def load_enrollments():
    if ENROLLMENT_FILE.exists():
        with open(ENROLLMENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_enrollments(data):
    with open(ENROLLMENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@router.message(F.text == "📥 Kursga yozilish")
async def enroll_in_course(message: Message):
    user_id = message.from_user.id

    # Foydalanuvchi ro‘yxatdan o‘tganmi?
    if not is_registered(user_id):
        await message.answer("📝 Kursga yozilish uchun avval ro‘yxatdan o‘ting.")
        await message.answer("Ismingizni yuboring:")
        # 👉 Bu yerda FSM orqali ro‘yxatdan o‘tkazish kerak bo‘ladi
        return

    # Allaqachon yozilganmi?
    enrollments = load_enrollments()
    if any(e["id"] == user_id for e in enrollments):
        await message.answer("❗️Siz allaqachon kursga yozilgansiz. Tez orada admin siz bilan bog‘lanadi.")
        return

    # Kurs nomi aniqlanadi (reply bo‘lsa)
    kurs_nomi = message.reply_to_message.text.split("kursi")[0].strip() if message.reply_to_message else "Kurs nomi"

    user = get_user_data(user_id)

    # Adminga yuboriladigan matn
    text = (
        f"📥 <b>Yangi kursga yozilish:</b>\n"
        f"👤 Ism: {user.get('name')}\n"
        f"📞 Telefon: {user.get('phone')}\n"
        f"📚 Kurs: <b>{kurs_nomi}</b>\n"
        f"🆔 ID: <code>{user_id}</code>\n"
        f"🔗 <a href='tg://user?id={user_id}'>Foydalanuvchi profili</a>\n\n"
        f"✅ Tasdiqlash: /confirm_{user_id}_{kurs_nomi.replace(' ', '_')}\n"
        f"❌ Bekor qilish: /cancel_{user_id}"
    )

    await message.bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="HTML")
    await message.answer("✅ Arizangiz yuborildi! Tez orada siz bilan bog‘lanamiz.", reply_markup=main_menu_keyboard("uz"))
