from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from bot.keyboards import main_menu_keyboard, language_keyboard

router = Router()

# Sozlamalar menyusi
@router.message(F.text.in_(["⚙️ Sozlamalar", "⚙️ Настройки", "⚙️ Settings"]))
async def show_settings_menu(message: Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌐 Tilni o‘zgartirish")],
            [KeyboardButton(text="🔔 Xabarnomalar"), KeyboardButton(text="⏰ Eslatmalar")],
            [KeyboardButton(text="📘 Mening kurslarim")],
            [KeyboardButton(text="🚪 Botdan chiqish")],
            [KeyboardButton(text="🏠 Asosiy menyu")]
        ],
        resize_keyboard=True
    )
    await message.answer("⚙️ Sozlamalar menyusiga xush kelibsiz!", reply_markup=markup)

# 1. Tilni o‘zgartirish
@router.message(F.text == "🌐 Tilni o‘zgartirish")
async def change_language(message: Message):
    await message.answer("Iltimos, tilni tanlang:", reply_markup=language_keyboard())

# 2. Xabarnomalar
@router.message(F.text == "🔔 Xabarnomalar")
async def toggle_notifications(message: Message):
    await message.answer("🔔 Xabarnomalar hozircha faollashtirilmagan. (Bu funksiya tez orada ishga tushadi)")

# 3. Eslatmalar
@router.message(F.text == "⏰ Eslatmalar")
async def toggle_reminders(message: Message):
    await message.answer("⏰ Eslatmalar funksiyasi hozircha mavjud emas.")

# 4. Mening kurslarim (data/enrollments.json asosida)
import json
from pathlib import Path

ENROLLMENT_FILE = Path("data/enrollments.json")

def load_enrollments():
    if ENROLLMENT_FILE.exists():
        with open(ENROLLMENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@router.message(F.text == "📘 Mening kurslarim")
async def my_courses(message: Message):
    user_id = message.from_user.id
    enrollments = load_enrollments()
    user_courses = [e["course"] for e in enrollments if e["id"] == user_id]

    if not user_courses:
        await message.answer("📭 Siz hech qanday kursga yozilmagansiz.")
    else:
        text = "📘 Siz yozilgan kurslar:\n" + "\n".join(f"✅ {c}" for c in user_courses)
        await message.answer(text)

# 5. Botdan chiqish
@router.message(F.text == "🚪 Botdan chiqish")
async def exit_bot(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("👋 Botdan chiqdingiz. Qaytadan boshlash uchun /start buyrug‘ini bosing.")
