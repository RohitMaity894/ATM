"""
test_auth.py
------------
Tests for auth.py: account creation, PIN lockout after 3 failed attempts, and admin login. File writes are patched out so tests
never touch the real atm_database.json
"""
import os
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import _new_database
from auth import create_account, login_existing, admin_login
from constants import DEFAULT_ADMIN_PIN
def fresh_db():
    return _new_database()
class TestCreateAccount(unittest.TestCase):
    @patch("auth.save_db")
    @patch("builtins.input", side_effect=["Alice", "1111", "1111"])
    def test_creates_account_with_starting_balance(self, mock_input, mock_save):
        db = fresh_db()
        acc_num = create_account(db)
        account = db["accounts"][acc_num]
        self.assertEqual(account["name"], "Alice")
        self.assertEqual(account["balance"], 5000.0)
        self.assertFalse(account["blocked"])
    @patch("auth.save_db")
    @patch("builtins.input", side_effect=["Bob", "2222", "2222"])
    def test_account_numbers_increment(self, mock_input, mock_save):
        db = fresh_db()
        first = int(create_account(db))
        with patch("builtins.input", side_effect=["Carol", "3333", "3333"]):
            second = int(create_account(db))
        self.assertEqual(second, first + 1)
class TestLoginLockout(unittest.TestCase):
    def _make_account(self, db):
        """Helper: create a known test account without touching disk."""
        with patch("auth.save_db"), \
             patch("builtins.input", side_effect=["Dave", "5555", "5555"]):
            return create_account(db)
    @patch("auth.save_db")
    def test_correct_pin_logs_in(self, mock_save):
        db = fresh_db()
        acc_num = self._make_account(db)
        with patch("builtins.input", side_effect=[acc_num, "5555"]):
            result = login_existing(db)
        self.assertEqual(result, acc_num)
    @patch("auth.save_db")
    def test_account_blocks_after_three_wrong_pins(self, mock_save):
        db = fresh_db()
        acc_num = self._make_account(db)
        with patch("builtins.input", side_effect=[acc_num, "0000", "0000", "0000"]):
            result = login_existing(db)
        self.assertIsNone(result)
        self.assertTrue(db["accounts"][acc_num]["blocked"])
    @patch("auth.save_db")
    def test_blocked_account_cannot_login_even_with_right_pin(self, mock_save):
        db = fresh_db()
        acc_num = self._make_account(db)
        db["accounts"][acc_num]["blocked"] = True
        with patch("builtins.input", side_effect=[acc_num]):
            result = login_existing(db)
        self.assertIsNone(result)
    @patch("auth.save_db")
    def test_unknown_account_number_returns_none(self, mock_save):
        db = fresh_db()
        with patch("builtins.input", side_effect=["9999999"]):
            result = login_existing(db)
        self.assertIsNone(result)
class TestAdminLogin(unittest.TestCase):
    def test_correct_admin_pin_succeeds(self):
        db = fresh_db()
        with patch("builtins.input", side_effect=[DEFAULT_ADMIN_PIN]):
            self.assertTrue(admin_login(db))
    def test_wrong_admin_pin_fails(self):
        db = fresh_db()
        with patch("builtins.input", side_effect=["0000"]):
            self.assertFalse(admin_login(db))
    @patch("auth.save_db")
    def test_login_existing_routes_admin_keyword_to_admin_login(self, mock_save):
        db = fresh_db()
        with patch("builtins.input", side_effect=["admin", DEFAULT_ADMIN_PIN]):
            result = login_existing(db)
        self.assertEqual(result, "admin")
if __name__ == "__main__":
    unittest.main()