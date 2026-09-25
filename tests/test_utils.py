"""
test_utils.py
-------------
Unit tests for the pure helper functions in utils.py: PIN hashing,currency formatting, and PIN validation. 
These have no side effects,so no database or file mocking is needed.
"""
import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import hash_pin, fmt, is_valid_pin
class TestHashPin(unittest.TestCase):
    def test_same_pin_produces_same_hash(self):
        self.assertEqual(hash_pin("1234"), hash_pin("1234"))
    def test_different_pins_produce_different_hashes(self):
        self.assertNotEqual(hash_pin("1234"), hash_pin("4321"))
    def test_hash_is_not_the_raw_pin(self):
        self.assertNotEqual(hash_pin("1234"), "1234")
    def test_hash_output_length(self):
        # SHA-256 hex digest only (64 chara)
        self.assertEqual(len(hash_pin("1234")), 64)
class TestFmt(unittest.TestCase):
    def test_formats_with_two_decimals(self):
        self.assertEqual(fmt(5000), "Rs. 5,000.00")
    def test_formats_with_thousands_separator(self):
        self.assertEqual(fmt(1234567.5), "Rs. 1,234,567.50")
    def test_formats_zero(self):
        self.assertEqual(fmt(0), "Rs. 0.00")
class TestIsValidPin(unittest.TestCase):
    def test_valid_four_digit_pin(self):
        self.assertTrue(is_valid_pin("1234"))
    def test_rejects_short_pin(self):
        self.assertFalse(is_valid_pin("123"))
    def test_rejects_long_pin(self):
        self.assertFalse(is_valid_pin("123456"))
    def test_rejects_non_numeric_pin(self):
        self.assertFalse(is_valid_pin("abcd"))
    def test_rejects_empty_string(self):
        self.assertFalse(is_valid_pin(""))
if __name__ == "__main__":
    unittest.main()