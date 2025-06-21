from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.states.registration import Registration
from bot.keyboards import main_menu_keyboard
from bot.config import ADMIN_ID
from bot.utils.registration_db import is_registered, save_user

router = Router()

@router.message(F.text == "📝 Ro‘yxatdan o‘tish")
async def start_registration(message: Message, state: FSMContext):
    await message.answer("👤 Iltimos, to‘liq ismingizni yuboring:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Registration.full_name)

@router.message(Registration.full_name)
async def ask_phone_number(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)

    contact_btn = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("📱 Telefon raqamingizni yuboring:", reply_markup=contact_btn)
    await state.set_state(Registration.phone_number)

@router.message(Registration.phone_number, F.contact)
async def finish_registration(message: Message, state: FSMContext):
    data = await state.get_data()
    full_name = data["full_name"]
    phone = message.contact.phone_number
    user_id = message.from_user.id
    username = message.from_user.username or "yo'q"

    # Raqam avval ro‘yxatdan o‘tganmi?
    if is_registered(phone):
        await message.answer("❗️Siz allaqachon ro‘yxatdan o‘tgansiz.", reply_markup=main_menu_keyboard("uz"))
        await state.clear()
        return

    # Yangi foydalanuvchini saqlash
    save_user({
        "id": user_id,
        "name": full_name,
        "phone": phone
    })

    msg = f"""🆕 <b>Yangi ro'yxatdan o'tish:</b>
👤 Ism: <b>{full_name}</b>
📞 Raqam: <b>{phone}</b>
🔗 Telegram: <a href="tg://user?id={user_id}">{username}</a>
"""
    await message.bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="HTML")

    await message.answer("✅ Ro‘yxatdan o‘tish muvaffaqiyatli yakunlandi!", reply_markup=main_menu_keyboard("uz"))
    await state.clear()
