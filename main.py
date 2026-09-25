"""
main.py
-------
Entry point. Ties together the database, auth, user_ops, and admin_ops
modules into the top-level loop. Run this file to start the ATM.

Author: Rohit Maity (26BCE11118)
"""

from database import load_db
from auth import login_existing, create_account
from user_ops import user_menu
from admin_ops import admin_menu


def main() -> None:
    db = load_db()
    while True:
        print("\n===== WELCOME TO THE ATM =====")
        print("1. Existing Account")
        print("2. New Account")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            acc_num = login_existing(db)
            if acc_num == "admin":
                admin_menu(db)
            elif acc_num is not None:
                user_menu(db, acc_num)

        elif choice == '2':
            acc_num = create_account(db)
            user_menu(db, acc_num)

        elif choice == '3':
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
