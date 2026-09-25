"""
database.py
-----------
Persistence layer. All reads/writes to the JSON "database" go through this module so the rest of the codebase never touches the
file format directly. Swapping this for a real database later only means editing this one file.
"""
import json
import os
from constants import DB_FILE, FIRST_ACCOUNT_NUMBER, DEFAULT_ADMIN_PIN
from utils import hash_pin
def _new_database() -> dict:
    """Blank database structure used on first run."""
    return {
        "next_acc_num": FIRST_ACCOUNT_NUMBER,
        "accounts": {},
        "admin": {"pin_hash": hash_pin(DEFAULT_ADMIN_PIN)},
    }
def load_db(path: str = DB_FILE) -> dict:
    """Load the database from disk, creating it if it doesn't exist yet."""
    if not os.path.exists(path):
        db = _new_database()
        save_db(db, path)
        return db
    with open(path, "r") as f:
        return json.load(f)
def save_db(db: dict, path: str = DB_FILE) -> None:
    """Persist the database to disk as pretty-printed JSON."""
    with open(path, "w") as f:
        json.dump(db, f, indent=2)
def get_account(db: dict, acc_num: str) -> dict | None:
    """Look up an acc by num. Returns None if it doesn't exist."""
    return db["accounts"].get(acc_num)
def generate_account_number(db: dict) -> str:
    """Reserve and return the next available acc num."""
    acc_num = str(db["next_acc_num"])
    db["next_acc_num"] += 1
    return acc_num