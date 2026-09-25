"""
admin_ops.py
------------
The admin menu and the management operations it offers: listing all
users, forcing a password reset, unblocking a locked account, and
viewing any user's transaction history.
"""
from database import save_db
from utils import now, fmt
def list_users(db: dict) -> None:
    accounts = db["accounts"]
    if not accounts:
        print("No users registered yet.")
        return
    print("\n--- Registered Users ---")
    for num, acc in accounts.items():
        status = "BLOCKED" if acc["blocked"] else "active"
        last = acc["last_login"] or "never"
        print(f"Acc# {num} | {acc['name']} | Balance {fmt(acc['balance'])} "
              f"| Status: {status} | Last login: {last}")
def reset_user_password(db: dict) -> None:
    num = input("Enter account number to reset password for: ").strip()
    acc = db["accounts"].get(num)
    if acc is None:
        print("No such account.")
        return
    acc["force_reset"] = True
    save_db(db)
    print(f"Password reset flag set for account {num}.")
    print("The user will be asked to set a new PIN on their next login.")
def unblock_user(db: dict) -> None:
    num = input("Enter account number to unblock: ").strip()
    acc = db["accounts"].get(num)
    if acc is None:
        print("No such account.")
        return
    if not acc["blocked"]:
        print("This account is not blocked.")
        return
    acc["blocked"] = False
    acc["attempts"] = 0
    acc["history"].append(f"[{now()}] Account unblocked by admin")
    save_db(db)
    print(f"Account {num} has been unblocked.")
def view_user_history(db: dict) -> None:
    num = input("Enter account number to view history: ").strip()
    acc = db["accounts"].get(num)
    if acc is None:
        print("No such account.")
        return
    print(f"\n--- History for {acc['name']} (Acc# {num}) ---")
    for entry in acc["history"]:
        print(entry)
def admin_menu(db: dict) -> None:
    """Main interactive loop for the admin. Returns on Exit."""
    actions = {
        '1': lambda: list_users(db),
        '2': lambda: reset_user_password(db),
        '3': lambda: unblock_user(db),
        '4': lambda: view_user_history(db),
    }
    while True:
        print("\n===== ADMIN MENU =====")
        print("1. Check Users (list all accounts)")
        print("2. Reset a User's Password")
        print("3. Unblock a User Account")
        print("4. View a User's History")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '5':
            print("Logging out of admin panel...")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice!")