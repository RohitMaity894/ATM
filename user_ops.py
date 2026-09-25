"""
user_ops.py
-----------
The logged-in user's menu and the banking operations it offers:
check balance, deposit, withdraw, view history, change password.
Each operation is a small standalone function so it can be tested
and reasoned about independently of the menu loop.
"""

from database import save_db
from utils import hash_pin, now, fmt, read_amount, set_new_pin


def check_balance(account: dict) -> None:
    print("Balance =", fmt(account["balance"]))


def deposit(db: dict, account: dict) -> None:
    amount = read_amount("Enter deposit amount: ")
    if amount is None:
        return
    account["balance"] += amount
    account["history"].append(f"[{now()}] Deposited {fmt(amount)}")
    save_db(db)
    print("Deposit successful! Balance =", fmt(account["balance"]))


def withdraw(db: dict, account: dict) -> None:
    amount = read_amount("Enter withdrawal amount: ")
    if amount is None:
        return
    if amount > account["balance"]:
        print("Insufficient balance!")
        return
    account["balance"] -= amount
    account["history"].append(f"[{now()}] Withdrew {fmt(amount)}")
    save_db(db)
    print("Withdrawal successful! Balance =", fmt(account["balance"]))


def show_history(account: dict) -> None:
    print("\n--- Transaction History ---")
    if not account["history"]:
        print("No transactions yet.")
        return
    for entry in account["history"]:
        print(entry)


def change_password(db: dict, account: dict) -> None:
    old_pin = input("Enter current PIN: ").strip()
    if hash_pin(old_pin) != account["pin_hash"]:
        print("Incorrect current PIN. Password not changed.")
        return
    new_pin = set_new_pin()
    account["pin_hash"] = hash_pin(new_pin)
    account["history"].append(f"[{now()}] Password changed by user")
    save_db(db)
    print("Password changed successfully!")


def user_menu(db: dict, acc_num: str) -> None:
    """Main interactive loop for a logged-in user. Returns on Exit."""
    account = db["accounts"][acc_num]
    actions = {
        '1': lambda: check_balance(account),
        '2': lambda: deposit(db, account),
        '3': lambda: withdraw(db, account),
        '4': lambda: show_history(account),
        '5': lambda: change_password(db, account),
    }

    while True:
        print("\n===== ATM MENU =====")
        print(f"Account: {acc_num}  |  Holder: {account['name']}")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transaction History")
        print("5. Change Password")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '6':
            print("Thank you for using the ATM. Logging out...")
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice!")
