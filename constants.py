"""
constants.py
------------
Central configuration values for the ATM system. Keeping these in one place makes the system easy to tune without touching business logic.
"""
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "atm_database.json")
STARTING_BALANCE = 5000.0
MAX_ATTEMPTS = 3
FIRST_ACCOUNT_NUMBER = 1001001
DEFAULT_ADMIN_PIN = "1234"
