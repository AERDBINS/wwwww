from aiogram import Router, F
from aiogram.types import Message
from bot.config import ADMIN_ID
from pathlib import Path
import json

router = Router()

ENROLLMENT_FILE = Path("data/enrollments.json")

def load_enrollments():
    if ENROLLMENT_FILE.exists():
        with open(ENROLLMENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@router.message(F.text == "/kurslar")
async def show_courses_for_admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    enrollments = load_enrollments()
    if not enrollments:
        await message.answer("📭 Hozircha hech kim kurslarga yozilmagan.")
        return

    # Kurslar bo‘yicha guruhlash
    kurslar = {}
    for item in enrollments:
        kurs = item["course"]
        if kurs not in kurslar:
            kurslar[kurs] = []
        kurslar[kurs].append(item)

    text = "📊 <b>Kurslar bo‘yicha ro‘yxat:</b>\n"
    for kurs, users in kurslar.items():
        text += f"\n📘 <b>{kurs}</b> — {len(users)} ta foydalanuvchi:\n"
        for i, u in enumerate(users, start=1):
            name = u.get("name", "Noma'lum")
            phone = u.get("phone", "—")
            status = u.get("paid", False)
            holat = "✅ To‘langan" if status else "❌ To‘lanmagan"
            text += f"{i}. {name} | {phone} | {holat}\n"

    await message.answer(text, parse_mode="HTML")
