from aiogram import Router, F
from aiogram.types import Message
from bot.config import ADMIN_ID
from pathlib import Path
import json

router = Router()

# 📞 Admin bilan aloqa
@router.message(F.text.in_(["📞 Admin bilan aloqa", "📞 Связаться с админом", "📞 Contact Admin"]))
async def contact_admin(message: Message):
    await message.answer(
        "📩 Admin bilan bog‘lanish uchun shu havolani bosing:\n"
        "https://t.me/aerdbins"  # username o‘rnida sizning admin havolangiz
    )

# 📂 Fayl manzili
ENROLLMENT_FILE = Path("data/enrollments.json")

# 🔄 Foydalanuvchilarni yuklash
def load_enrollments():
    if ENROLLMENT_FILE.exists():
        with open(ENROLLMENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 💾 Foydalanuvchilarni saqlash
def save_enrollments(data):
    with open(ENROLLMENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ✅ Kursga tasdiqlash
@router.message(F.text.startswith("/confirm_"))
async def confirm_course(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        _, user_id_str, kurs_raw = message.text.split("_", 2)
        user_id = int(user_id_str)
        kurs_nomi = kurs_raw.replace("_", " ")
    except Exception:
        await message.answer("❌ Noto‘g‘ri format. /confirm_<id>_<kurs>")
        return

    enrollments = load_enrollments()

    if any(e["id"] == user_id and e["course"] == kurs_nomi for e in enrollments):
        await message.answer("⚠️ Bu foydalanuvchi bu kursga allaqachon tasdiqlangan.")
        return

    enrollments.append({
        "id": user_id,
        "course": kurs_nomi
    })
    save_enrollments(enrollments)

    await message.bot.send_message(
        user_id,
        f"✅ Siz <b>{kurs_nomi}</b> kursiga muvaffaqiyatli yozildingiz!",
        parse_mode="HTML"
    )
    await message.answer("☑️ Foydalanuvchi tasdiqlandi.")

# ❌ Bekor qilish
@router.message(F.text.startswith("/cancel_"))
async def cancel_course(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(message.text.split("_")[1])
    except Exception:
        await message.answer("❌ Format xato. /cancel_<id>")
        return

    await message.bot.send_message(user_id, "❌ Kursga yozilish so‘rovingiz rad etildi.")
    await message.answer("🚫 Bekor qilindi.")
