import unittest
from modules import helper


class TestHelper(unittest.TestCase):

    def test_valid_port_numbers(self):
        valid_port_numbers = list(range(helper.MIN_PORT, helper.MAX_PORT+1))
        for port in valid_port_numbers:
            self.assertIsNone(helper.validate_port(port), msg=f"Failed on {port}")

    def test_invalid_port_numbers(self):
        invalid_port_numbers = [-1, -80, 0, 65536, 70000, 99999, 2**16, 10**6]
        for port in invalid_port_numbers:
            with self.assertRaises(ValueError, msg=f"Failed on {port}"):
                helper.validate_port(port)

    def test_invalid_port_values(self):
        invalid_port_values = [None, "", "80", "65536", "http", 22.5, float("inf"), float("nan"), [], {}, True, False]
        for value in invalid_port_values:
            with self.assertRaises(TypeError, msg=f"Failed on {value}"):
                helper.validate_port(value)