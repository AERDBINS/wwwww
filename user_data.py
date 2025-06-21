# user_data.py
registered_users = {}

def is_registered(user_id: int) -> bool:
    return user_id in registered_users

def register_user(user_id: int, data: dict):
    registered_users[user_id] = data

def get_user_data(user_id: int) -> dict:
    return registered_users.get(user_id, {})
