
# ATM Simulator — Multi-User Edition with Admin Panel
**Author:** Rohit Maity (26BCE11118)
---------------------------------------------------------------------
A console-based, multi-user ATM system written in Python. Supports
account registration, secure PIN login with lockout, everyday banking
operations, and an admin role for account recovery — with all data
persisted to a local JSON file between runs.

## Overview
Unlike a typical single-account ATM script, this project models a
small real banking system: any number of users can register their own
account, log in with their own account number and PIN, and manage
their own balance independently. A separate **admin** account can
oversee all users — listing them, resetting a forgotten password, or
unblocking an account that locked itself after too many failed PIN
attempts. See [`statement.md`](statement.md) for the full problem
statement and scope, and [`Project_Report.pdf`](Project_Report.pdf)
for the full write-up with diagrams.

## Features
- **Account registration** with an auto-generated account number and a
  self-chosen 4-digit PIN
- **Secure login** — PINs are SHA-256 hashed, never stored or compared
  in plain text
- **Account lockout** after 3 failed PIN attempts (only an admin can
  unblock it)
- **Core banking operations** — check balance, deposit, withdraw
  (with an insufficient-balance guard)
- **Transaction history** with timestamps, per account
- **Self-service PIN change** (requires the current PIN)
- **Admin panel**:
  - list every registered user with balance/status/last login
  - force a password reset on a specific account
  - unblock a locked account
  - view any individual user's transaction history
- **Persistent storage** — accounts and history survive between runs
  via `atm_database.json`, created automatically on first run
- **Modular codebase** — 7 focused modules instead of one large script
- **Unit tested** — 29 tests covering hashing, validation, lockout
  logic, deposits/withdrawals, and password changes

## Technologies / Tools Used
- **Python 3.10+** (standard library only — `hashlib`, `json`, `os`,
  `datetime`)
- **unittest** and **unittest.mock** for the test suite
- **matplotlib** — used only to generate the design diagrams in
  `diagrams/` (not a runtime dependency of the ATM itself)
- **Git** for version control

## Project Structure
```
├── main.py                # Entry point / top-level menu
├── constants.py           # Configuration values
├── utils.py               # Hashing, formatting, input validation helpers
├── database.py            # JSON persistence layer
├── auth.py                # Login, registration, admin authentication
├── user_ops.py            # User menu: balance, deposit, withdraw, history, PIN
├── admin_ops.py           # Admin menu: list users, reset, unblock, history
├── statement.md           # Problem statement, scope, target users, features
├── README.md              # This file
├── tests/
│   ├── test_utils.py
│   ├── test_auth.py
│   └── test_user_ops.py
└── diagrams/
    ├── architecture.png
    ├── workflow.png
    ├── use_case.png
    ├── class_diagram.png
    ├── er_diagram.png
    └── generate_diagrams.py   # Script that renders the diagrams above
```
## Steps to Install & Run
1. Make sure you have **Python 3.10 or newer** installed:
   ```
   python3 --version
   ```
2. Clone or download this repository, then move into it:
   ```
   cd atm_project
   ```
3. Run the program (no external dependencies needed to run the ATM itself):
   ```
   python3 main.py
   ```
4. On first run, follow the prompts:
   - Choose **2. New Account** to register (name + set a 4-digit PIN)
   - Or choose **1. Existing Account** to log in with an account number
     you already created
   - Type `admin` as the account number at the login prompt to access
     the admin panel (default admin PIN: `1234`)
Your data is saved automatically to `atm_database.json` in the same
folder — delete that file at any time to reset the system.

## Instructions for Testing
The project ships with 29 unit tests covering the core logic (PIN
hashing/validation, currency formatting, account creation, login
lockout after 3 failed attempts, admin login, deposits, withdrawals,
and password changes). Tests use mocked input and mocked file writes,
so running them never touches your real `atm_database.json`.
Run the full suite from the project root:
```
python3 -m unittest discover -s tests -v
```
Expected result: `Ran 29 tests ... OK`

## Screenshots
See the `diagrams/` folder for the system architecture, workflow,
use case, class, and ER diagrams referenced in the project report.

## Notes on Security Scope
This is an academic/demo project, not production banking software:
PINs are hashed (SHA-256) but the JSON file is not encrypted at rest,
and there is no protection against concurrent multi-process writes.
See `statement.md` for the full scope statement.