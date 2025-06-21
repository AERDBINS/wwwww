from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

# Inline tarzda kanalga o‘tish + tasdiqlash tugmasi
def subscribe_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Kanalga o‘tish", url="https://t.me/aaerdbins")],
            [InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_subscription")]
        ]
    )

# 1. Til tanlash uchun tugmalar
def language_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇺🇿 O‘zbek tili")],
            [KeyboardButton(text="🇷🇺 Русский язык")],
            [KeyboardButton(text="🇬🇧 English")]
        ],
        resize_keyboard=True
    )

# 2. Asosiy menyu (tilga qarab)
def main_menu_keyboard(lang: str):
    if lang == "uz":
        keyboard = [
            [KeyboardButton(text="🎓 O‘quv markazi haqida")],
            [KeyboardButton(text="📚 Kurslar"), KeyboardButton(text="🧪 Test")],
            [KeyboardButton(text="📝 Ro‘yxatdan o‘tish"), KeyboardButton(text="📞 Admin bilan aloqa")],
            [KeyboardButton(text="⚙️ Sozlamalar")]
        ]
    elif lang == "ru":
        keyboard = [
            [KeyboardButton(text="🎓️ О учебном центре")],
            [KeyboardButton(text="📚 Курсы"), KeyboardButton(text="🧪 Тест")],
            [KeyboardButton(text="📝 Регистрация"), KeyboardButton(text="📞 Связаться с админом")],
            [KeyboardButton(text="⚙️ Настройки")]
        ]
    elif lang == "en":
        keyboard = [
            [KeyboardButton(text="🎓️ About the center")],
            [KeyboardButton(text="📚 Courses"), KeyboardButton(text="🧪 Test")],
            [KeyboardButton(text="📝 Register"), KeyboardButton(text="📞 Contact Admin")],
            [KeyboardButton(text="⚙️ Settings")]
        ]
    else:
        keyboard = [
            [KeyboardButton(text="🎓️ O‘quv markazi haqida")],
            [KeyboardButton(text="📚 Kurslar"), KeyboardButton(text="🧪 Test")],
            [KeyboardButton(text="📝 Ro‘yxatdan o‘tish"), KeyboardButton(text="📞 Admin bilan aloqa")],
            [KeyboardButton(text="⚙️ Sozlamalar")]
        ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)




# 4. Asosiy menyuga qaytish
def back_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🏠 Asosiy menyu")]],
        resize_keyboard=True
    )
