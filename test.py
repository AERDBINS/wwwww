from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from bot.keyboards import main_menu_keyboard
from aiogram.fsm.context import FSMContext

router = Router()

# Testlar menyusi
@router.message(F.text.in_(["🧪 Test", "🧪 Тест", "🧪 Test"]))
async def show_test_menu(message: Message):
    text = message.text
    if text == "🧪 Test":
        lang = "uz"
    elif text == "🧪 Тест":
        lang = "ru"
    elif text == "🧪 Test":
        lang = "en"
    else:
        lang = "uz"

    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧮 Matematika testi"), KeyboardButton(text="🌍 Tarix testi")],
            [KeyboardButton(text="🔙 Ortga")]
        ],
        resize_keyboard=True
    )

    await message.answer("Quyidagi testlardan birini tanlang:", reply_markup=markup)

# Test boshlanishi (oddiy misol)
@router.message(F.text == "🧮 Matematika testi")
async def math_test(message: Message):
    await message.answer("❓ Savol 1: 5 + 7 = ?\n\nA) 10\nB) 11\nC) 12\nD) 13")

# Asosiy menyuga qaytish
@router.message(F.text == "🔙 Ortga")
async def back_to_main_menu(message: Message, state: FSMContext):
    # Lang aniqlashni siz FSM orqali saqlaysiz deb taxmin qilamiz.
    # Aks holda default — uz
    data = await state.get_data()
    lang = data.get("lang", "uz")

    await message.answer("🏠 Asosiy menyu", reply_markup=main_menu_keyboard(lang))
