from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Matn va tugmalar
about_text = (
    "📚 <b>O‘quv markazimiz</b> haqida ma’lumot:\n"
    "📌 Zamonaviy fanlar asosida o‘qitish\n"
    "👨‍🏫 Tajribali ustozlar\n"
    "🌐 Onlayn va oflayn darslar mavjud"
)

about_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📢 Telegram", url="https://t.me/aerdbins")],
    [InlineKeyboardButton(text="📸 Instagram", url="https://instagram.com/aerdbins")],
    [InlineKeyboardButton(text="▶️ YouTube", url="https://youtube.com/reaktoruz")],
    [InlineKeyboardButton(text="👨‍🏫 O‘qituvchilar haqida", callback_data="about_teachers")]
])

@router.message(F.text == "🎓 O‘quv markazi haqida")
async def about_handler(message: Message):
    await message.answer(about_text, reply_markup=about_buttons)

@router.callback_query(F.data == "about_teachers")
async def teachers_info(callback):
    await callback.message.edit_text(
        "👨‍🏫 Ustozlarimiz:\n\n"
        "• Alijonov Murod – Matematika\n"
        "• Karimova Shaxnoza – Ingliz tili\n"
        "• Rasulov Aziz – Fizika\n"
        "• ... (davomi bo‘ladi)"
    )
