import json
from pathlib import Path

DB_FILE = Path("users.json")

def load_users():
    if DB_FILE.exists():
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_user(user_data):
    users = load_users()
    users.append(user_data)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def is_registered(phone_number: str) -> bool:
    users = load_users()
    return any(user["phone"] == phone_number for user in users)
