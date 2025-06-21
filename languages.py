texts = {
    "subscribe_text": {
        "uz": "📢 Iltimos, kanalga obuna bo‘ling:",
        "ru": "📢 Пожалуйста, подпишитесь на канал:",
        "en": "📢 Please subscribe to the channel:"
    },
    "check_sub": {
        "uz": "✅ Obunani tekshirish",
        "ru": "✅ Проверить подписку",
        "en": "✅ Check subscription"
    },
    "go_to_channel": {
        "uz": "📢 Kanalga o‘tish",
        "ru": "📢 Перейти в канал",
        "en": "📢 Go to Channel"

    },

    "choose_course": {
        "uz": "📚 Fanlardan birini tanlang:",
        "ru": "📚 Выберите курс:",
        "en": "📚 Choose a course:"
    },
    "main_menu": {
        "uz": "🏠 Asosiy menyu",
        "ru": "🏠 Главное меню",
        "en": "🏠 Main menu"
    },

    "uz": {
        "start_text": "Assalomu alaykum! Botimizga xush kelibsiz. Davom etish uchun tilni tanlang:",
        "language_chosen": "Til muvaffaqiyatli o‘zgartirildi!",
        "subscribe_text": "Botdan foydalanishdan avval quyidagi kanalga obuna bo‘ling 👇",
        "check_sub": "✅ Obunani tekshirish",
        "main_menu": "🏠 Asosiy menyu",
        "menu_buttons": [
            "🎓 O‘quv markazi haqida",
            "📚 Kurslar",
            "📝 Ro‘yxatdan o‘tish",
            "🧪 Test",
            "💬 Admin bilan aloqa",
            "⚙️ Sozlamalar"
        ]
    },

    "ru": {
        "start_text": "Здравствуйте! Добро пожаловать в наш бот. Пожалуйста, выберите язык:",
        "language_chosen": "Язык успешно изменён!",
        "subscribe_text": "Пожалуйста, подпишитесь на канал, прежде чем продолжить 👇",
        "check_sub": "✅ Проверить подписку",
        "main_menu": "🏠 Главное меню",
        "menu_buttons": [
            "🎓 О учебном центре",
            "📚 Курсы",
            "📝 Регистрация",
            "🧪 Тест",
            "💬 Связаться с админом",
            "⚙️ Настройки"
        ]
    },

    "en": {
        "start_text": "Hello! Welcome to our bot. Please choose your language:",
        "language_chosen": "Language successfully changed!",
        "subscribe_text": "Please subscribe to the channel before continuing 👇",
        "check_sub": "✅ Check subscription",
        "main_menu": "🏠 Main Menu",
        "menu_buttons": [
            "🎓 About the Center",
            "📚 Courses",
            "📝 Register",
            "🧪 Test",
            "💬 Contact Admin",
            "⚙️ Settings"
        ]

    }
}

def get_text(key: str, lang: str = "uz") -> str | list:
    """Berilgan til va kalit bo‘yicha matnni qaytaradi."""
    return texts.get(lang, texts["uz"]).get(key, f"[{key}]")
