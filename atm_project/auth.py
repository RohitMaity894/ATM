"""
auth.py
-------
Everything related to proving identity: creating new accounts, logging
into an existing one (with lockout after repeated failures), and
admin authentication. Returns the authenticated account number (or
"admin") to the caller instead of driving the menu itself, so this
module stays focused purely on authentication.
"""

from constants import STARTING_BALANCE, MAX_ATTEMPTS
from database import save_db, generate_account_number
from utils import hash_pin, now, fmt, set_new_pin


def create_account(db: dict) -> str:
    """
    Register a new user account. Returns the new account number.
    """
    print("\n--- Create New Account ---")
    name = input("Enter your name: ").strip() or "Unnamed"
    acc_num = generate_account_number(db)

    pin = set_new_pin()
    db["accounts"][acc_num] = {
        "name": name,
        "pin_hash": hash_pin(pin),
        "balance": STARTING_BALANCE,
        "history": [f"[{now()}] Account created with balance {fmt(STARTING_BALANCE)}"],
        "attempts": 0,
        "blocked": False,
        "force_reset": False,
        "last_login": None,
    }
    save_db(db)

    print("\nAccount created successfully!")
    print("Account Holder:", name)
    print("Account Number:", acc_num)
    print("(Save this account number, you'll need it to log in)")
    return acc_num


def login_existing(db: dict):
    """
    Interactive login flow for an existing account.
    Returns the account number (str) on success, or None if login
    did not complete (not found, blocked, wrong PIN, cancelled).
    Handles the "admin" special-case account number by delegating
    to admin_login().
    """
    acc_num = input("\nEnter Account Number: ").strip()

    if acc_num.lower() == "admin":
        return "admin" if admin_login(db) else None

    account = db["accounts"].get(acc_num)
    if account is None:
        print("No account found with that number.")
        return None

    if account["blocked"]:
        print("This account is blocked due to too many failed attempts.")
        print("Please contact the admin to have it unblocked.")
        return None

    if account["force_reset"]:
        print("\nAn admin has reset your password.")
        print("Please set a new PIN to continue.")
        new_pin = set_new_pin()
        account["pin_hash"] = hash_pin(new_pin)
        account["force_reset"] = False
        account["attempts"] = 0
        account["last_login"] = now()
        account["history"].append(f"[{now()}] Password reset (admin-forced) and updated")
        save_db(db)
        print("PIN updated successfully. Logging you in...")
        return acc_num

    while account["attempts"] < MAX_ATTEMPTS:
        pin = input("Enter PIN: ").strip()
        if hash_pin(pin) == account["pin_hash"]:
            account["attempts"] = 0
            account["last_login"] = now()
            save_db(db)
            print(f"\nPIN Correct! Welcome, {account['name']}.")
            return acc_num

        account["attempts"] += 1
        remaining = MAX_ATTEMPTS - account["attempts"]
        if remaining > 0:
            print(f"Incorrect PIN! {remaining} attempt(s) remaining.")
        else:
            account["blocked"] = True
            print("Maximum attempts reached. Account Blocked!")
            print("Contact the admin to unblock this account.")
        save_db(db)

    return None


def admin_login(db: dict) -> bool:
    """Authenticate the admin account. Returns True on success."""
    pin = input("Enter Admin PIN: ").strip()
    if hash_pin(pin) != db["admin"]["pin_hash"]:
        print("Incorrect admin PIN.")
        return False
    print("\nWelcome, Admin.")
    return True
