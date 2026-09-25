# Problem Statement
Traditional beginner ATM simulation scripts model only a single hard-coded
account with an in-memory balance, so all data is lost the moment the
program exits and there is no way to manage more than one user. This
project builds a **multi-user ATM simulator** that supports account
creation, secure PIN-based login, everyday banking operations, and a
separate admin role for account recovery — with all data persisted
between runs.

## Scope of the Project
**In scope:**
- Multi-user account registration and login via a console interface
- Core banking operations: balance check, deposit, withdrawal
- Per-account transaction history
- PIN security: hashed storage, 3-attempt lockout, self-service PIN change
- An admin role that can list users, force a password reset, unblock a
  locked account, and inspect any user's history
- Persistent storage using a local JSON file (no external database
  server required)
**Out of scope:**
- A graphical or web user interface (console-only)
- Real banking integrations, multi-currency support, or interest
  calculations
- Concurrent/multi-terminal access to the same data file
- Production-grade encryption at rest (PINs are hashed, but the JSON
  file itself is not encrypted)

## Target Users
- **Bank customers (regular users)** — create an account, log in with
  their account number and PIN, and manage their own balance.
- **Bank administrator** — a single admin role responsible for
  onboarding oversight, resetting forgotten passwords, and unblocking
  accounts after failed login attempts.

## High-Level Features
1. **Account registration** — auto-generated account number, user sets
   their own 4-digit PIN, starting balance of Rs. 5,000.
2. **Secure login** — PIN is hashed (SHA-256) and never stored or
   compared in plain text; 3 failed attempts blocks the account.
3. **Banking operations** — check balance, deposit, withdraw (with an
   insufficient-funds guard), and view a timestamped transaction history.
4. **Self-service PIN change** — requires the current PIN to confirm
   identity before setting a new one.
5. **Admin panel** — list all registered users, force a password reset
   on a specific account, unblock a locked account, and view any
   individual user's transaction history.
6. **Persistence** — all accounts and history survive between program
   runs via a local JSON database file.