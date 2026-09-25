"""
test_user_ops.py
-----------------
Tests for user_ops.py: deposit, withdraw (including the insufficient balance guard), and password change. Uses a bare in-memory
acc dict rather than the full database, and patches save_db so no file I/O happens during tests
"""
import os
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import hash_pin
from user_ops import deposit, withdraw, change_password
def sample_account():
    return {
        "name": "Test User",
        "pin_hash": hash_pin("1234"),
        "balance": 1000.0,
        "history": [],
        "attempts": 0,
        "blocked": False,
        "force_reset": False,
        "last_login": None,
    }
class TestDeposit(unittest.TestCase):
    @patch("user_ops.save_db")
    @patch("builtins.input", return_value="500")
    def test_deposit_increases_balance(self, mock_input, mock_save):
        account = sample_account()
        deposit({}, account)
        self.assertEqual(account["balance"], 1500.0)
    @patch("user_ops.save_db")
    @patch("builtins.input", return_value="-50")
    def test_negative_deposit_is_rejected(self, mock_input, mock_save):
        account = sample_account()
        deposit({}, account)
        self.assertEqual(account["balance"], 1000.0)  # unchanged
    @patch("user_ops.save_db")
    @patch("builtins.input", return_value="abc")
    def test_non_numeric_deposit_is_rejected(self, mock_input, mock_save):
        account = sample_account()
        deposit({}, account)
        self.assertEqual(account["balance"], 1000.0)  # unchanged
class TestWithdraw(unittest.TestCase):
    @patch("user_ops.save_db")
    @patch("builtins.input", return_value="400")
    def test_withdraw_decreases_balance(self, mock_input, mock_save):
        account = sample_account()
        withdraw({}, account)
        self.assertEqual(account["balance"], 600.0)
    @patch("user_ops.save_db")
    @patch("builtins.input", return_value="5000")
    def test_withdraw_more_than_balance_is_rejected(self, mock_input, mock_save):
        account = sample_account()
        withdraw({}, account)
        self.assertEqual(account["balance"], 1000.0)  # unchanged
    @patch("user_ops.save_db")
    @patch("builtins.input", return_value="1000")
    def test_withdraw_exact_balance_is_allowed(self, mock_input, mock_save):
        account = sample_account()
        withdraw({}, account)
        self.assertEqual(account["balance"], 0.0)
class TestChangePassword(unittest.TestCase):
    @patch("user_ops.save_db")
    @patch("builtins.input", side_effect=["1234", "9999", "9999"])
    def test_correct_old_pin_allows_change(self, mock_input, mock_save):
        account = sample_account()
        change_password({}, account)
        self.assertEqual(account["pin_hash"], hash_pin("9999"))
    @patch("user_ops.save_db")
    @patch("builtins.input", return_value="0000")
    def test_wrong_old_pin_blocks_change(self, mock_input, mock_save):
        account = sample_account()
        original_hash = account["pin_hash"]
        change_password({}, account)
        self.assertEqual(account["pin_hash"], original_hash)
if __name__ == "__main__":
    unittest.main()