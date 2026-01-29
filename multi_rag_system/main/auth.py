import hashlib
import json
import os

USER_DB_PATH = "data/users.json"

def _hash_password(password):
    """Encrypts a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def _load_users():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(USER_DB_PATH):
        with open(USER_DB_PATH, "r") as f:
            return json.load(f)
    return {}

def signup(username, password):
    """Registers a new user if the username isn't taken."""
    users = _load_users()
    if username in users:
        return False, "User already exists."
    users[username] = _hash_password(password)
    with open(USER_DB_PATH, "w") as f:
        json.dump(users, f)
    return True, "Sign up successful!"

def login(username, password):
    """Verifies credentials against the stored hash."""
    users = _load_users()
    if username in users and users[username] == _hash_password(password):
        return True
    return False