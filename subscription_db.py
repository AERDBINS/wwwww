import json
from pathlib import Path

DB_FILE = Path("subscribed_users.json")

def load_subscribed():
    if DB_FILE.exists():
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_subscriber(user_id):
    users = load_subscribed()
    if user_id not in users:
        users.append(user_id)
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f)

def is_subscribed(user_id):
    return user_id in load_subscribed()
