"""
utils.py
--------
Small, dependency-free helper functions used across the ATM system:
PIN hashing, timestamps, currency formatting, and validated input readers.
Keeping these separate makes them independently unit-testable.
"""

import hashlib
from datetime import datetime


def hash_pin(pin: str) -> str:
    """Return a SHA-256 hash of a PIN. Raw PINs are never stored."""
    return hashlib.sha256(pin.encode()).hexdigest()


def now() -> str:
    """Current timestamp as a readable string, used for history logs."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def fmt(amount: float) -> str:
    """Format a number as currency, e.g. 5000 -> 'Rs. 5,000.00'."""
    return f"Rs. {amount:,.2f}"


def is_valid_pin(pin: str) -> bool:
    """A valid PIN is exactly 4 digits."""
    return pin.isdigit() and len(pin) == 4


def read_pin(prompt: str) -> str:
    """Prompt until the user enters a valid 4-digit PIN."""
    while True:
        pin = input(prompt).strip()
        if is_valid_pin(pin):
            return pin
        print("PIN must be exactly 4 digits.")


def read_amount(prompt: str):
    """
    Prompt for a positive numeric amount.
    Returns the float, or None if the input was invalid (caller decides
    whether to re-prompt or abort the operation).
    """
    raw = input(prompt).strip()
    try:
        amount = float(raw)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return None
    if amount <= 0:
        print("Amount must be greater than zero.")
        return None
    return amount


def set_new_pin() -> str:
    """Prompt twice for a new PIN and confirm both entries match."""
    while True:
        pin1 = read_pin("Set a new 4-digit PIN: ")
        pin2 = read_pin("Confirm new PIN: ")
        if pin1 == pin2:
            return pin1
        print("PINs did not match, try again.")
