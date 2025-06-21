from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from pathlib import Path
import json

from bot.languages import get_text
from bot.keyboards import main_menu_keyboard
from bot.utils.registration_db import is_registered, load_users
from bot.states.registration import Registration
from bot.config import ADMIN_ID

router = Router()

# Kurslar va ma’lumotlari
courses = [
    "📊 Matematika",
    "🔭 Fizika",
    "🇬🇧 Ingliz tili",
    "📜 Tarix",
    "📚 Ona tili va adabiyot",
    "🚗 Haydovchilik testi"
]

course_texts = {
    "📊 Matematika": "📊 Matematika kursida siz algebra, geometriya, matematik tahlil o‘rganasiz.",
    "🔭 Fizika": "🔭 Fizika kursida mexanika, optika va elektr fizikasi o‘rganiladi.",
    "🇬🇧 Ingliz tili": "🇬🇧 Ingliz tili kursi: grammatika, so‘zlashuv, IELTS tayyorgarlik.",
    "📜 Tarix": "📜 Tarix kursi: jahon tarixi, O‘zbekiston tarixi.",
    "📚 Ona tili va adabiyot": "📚 Ona tili va adabiyot: nazariy bilimlar, matn tahlili.",
    "🚗 Haydovchilik testi": "🚗 Haydovchilik kursi: YHQ, nazariy testlar, amaliyot."
}

@router.message(F.text == "📚 Kurslar")
async def show_courses_menu(message: Message):
    lang = "uz"
    keyboard = []
    for i in range(0, len(courses), 2):
        row = [KeyboardButton(text=courses[i])]
        if i + 1 < len(courses):
            row.append(KeyboardButton(text=courses[i + 1]))
        keyboard.append(row)

    keyboard.append([KeyboardButton(text="🏠 Asosiy menyu")])
    markup = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder=get_text("choose_course", lang)
    )
    await message.answer(get_text("choose_course", lang), reply_markup=markup)

@router.message(F.text == "🏠 Asosiy menyu")
async def back_to_main_menu(message: Message):
    lang = "uz"
    await message.answer(get_text("main_menu", lang), reply_markup=main_menu_keyboard(lang))

@router.message(F.text.in_(courses))
async def course_info(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗕 Kursga yozilish")],
            [KeyboardButton(text="🔙 Ortga")]
        ],
        resize_keyboard=True
    )
    await message.answer(course_texts.get(message.text, "№ Ma'lumot topilmadi."), reply_markup=keyboard)

@router.message(F.text == "🗕 Kursga yozilish")
async def enroll_course(message: Message, state: FSMContext):
    user_id = message.from_user.id
    users = load_users()
    user_data = next((user for user in users if user["id"] == user_id), None)

    if user_data:
        data = await state.get_data()
        course = data.get("course", "Noma’lum kurs")

        msg = f"""\
📅 <b>Yangi kursga yozilish:</b>
👤 Ism: <b>{user_data['name']}</b>
📞 Tel: <b>{user_data['phone']}</b>
📚 Kurs: <b>{course}</b>
🔗 Telegram: <a href=\"tg://user?id={user_id}\">{user_id}</a>

✅ /confirm_{user_id}_{course.replace(' ', '_')}
❌ /cancel_{user_id}
💰 /pay_{user_id}
"""
        await message.bot.send_message(ADMIN_ID, msg, parse_mode="HTML")
        await message.answer("✅ Kursga yozildingiz! Tez orada siz bilan bog‘lanamiz.", reply_markup=main_menu_keyboard("uz"))
    else:
        await message.answer("❗️Siz hali ro‘yxatdan o‘tmagansiz. Iltimos, avval ro‘yxatdan o‘ting.")

@router.message(F.text == "🔙 Ortga")
async def back_to_courses(message: Message):
    await show_courses_menu(message)

ENROLLMENT_FILE = Path("data/enrollments.json")

def save_enrollments(data):
    ENROLLMENT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ENROLLMENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_enrollments():
    if ENROLLMENT_FILE.exists():
        with open(ENROLLMENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@router.message(F.text.startswith("/confirm_"))
async def confirm_course(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        _, user_id_str, kurs_raw = message.text.split("_", 2)
        user_id = int(user_id_str)
        course = kurs_raw.replace("_", " ")
    except:
        await message.answer("❌ Format xato. To‘g‘ri format: /confirm_<id>_<kurs>")
        return

    enrollments = load_enrollments()
    if any(e["id"] == user_id and e["course"] == course for e in enrollments):
        await message.answer("⚠️ Bu foydalanuvchi allaqachon tasdiqlangan.")
        return

    users = load_users()
    user_data = next((u for u in users if u["id"] == user_id), {})
    enrollments.append({
        "id": user_id,
        "course": course,
        "name": user_data.get("name", "Noma'lum"),
        "phone": user_data.get("phone", "—"),
        "paid": False
    })

    save_enrollments(enrollments)
    await message.bot.send_message(user_id, f"✅ Siz <b>{course}</b> kursiga muvaffaqiyatli yozildingiz!", parse_mode="HTML")
    await message.answer("☑️ Foydalanuvchi tasdiqlandi.")

@router.message(F.text.startswith("/cancel_"))
async def cancel_course(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        _, user_id_str, kurs_raw = message.text.split("_", 2)
        user_id = int(user_id_str)
        course = kurs_raw.replace("_", " ")
    except:
        await message.answer("❌ Format xato. To‘g‘ri format: /cancel_<id>_<kurs>")
        return

    enrollments = load_enrollments()
    new_enrollments = [
        e for e in enrollments if not (e["id"] == user_id and e["course"] == course)
    ]
    save_enrollments(new_enrollments)

    await message.bot.send_message(user_id, f"❌ Siz <b>{course}</b> kursidan chiqarildingiz.", parse_mode="HTML")
    await message.answer("🚫 Kurs bekor qilindi.")


@router.message(F.text.startswith("/pay_"))
async def mark_as_paid(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(message.text.split("_")[1])
    except:
        await message.answer("❌ Format xato. To‘g‘ri format: /pay_<id>")
        return

    enrollments = load_enrollments()
    updated = False
    for e in enrollments:
        if e["id"] == user_id:
            e["paid"] = True
            updated = True
            break

    if updated:
        save_enrollments(enrollments)
        await message.answer("✅ To‘lov holati yangilandi.")
    else:
        await message.answer("❗️ Foydalanuvchi topilmadi.")

@router.message(F.text == "📊 Statistika")
async def show_statistics(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ Sizga bu buyruq ruxsat etilmagan.")

    enrollments = load_enrollments()
    if not enrollments:
        return await message.answer("📭 Hali hech kim kursga yozilmagan.")

    stat_msg = "📊 <b>Kurslar bo‘yicha statistika:</b>\n\n"
    course_summary = {}

    for item in enrollments:
        course = item["course"]
        if course not in course_summary:
            course_summary[course] = {
                "total": 0,
                "paid": 0,
                "students": []
            }

        course_summary[course]["total"] += 1
        if item.get("paid"):
            course_summary[course]["paid"] += 1

        course_summary[course]["students"].append(item)

    for course, data in course_summary.items():
        stat_msg += f"📘 <b>{course}</b>\n"
        stat_msg += f"👥 Jami: <b>{data['total']}</b> | 💳 To‘laganlar: <b>{data['paid']}</b>\n"

        for s in data["students"]:
            status = "✅" if s.get("paid") else "❌"
            stat_msg += f"— {s['name']} | {s['phone']} | {status}\n"

        stat_msg += "\n"

    await message.answer(stat_msg, parse_mode="HTML")
