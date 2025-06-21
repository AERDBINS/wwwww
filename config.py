import os
from dotenv import load_dotenv

load_dotenv()  # .env fayldan o‘qish

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

LANGUAGES = ["uz", "ru", "en"]
DEFAULT_LANG = "uz"


