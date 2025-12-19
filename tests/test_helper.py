import unittest
from modules import helper


class TestValidatePort(unittest.TestCase):

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


class TestValidatePortList(unittest.TestCase):
    
    def test_valid_port_list(self):
        valid_port_lists = [
            [1],
            [22, 80, 443],
            [1024, 2048, 65535],
            list(range(1, 1025)),
            [8080, 8443, 9000]
        ]

        for plist in valid_port_lists:
            self.assertIsNone(helper.validate_port_list(plist), msg=f"Failed on {plist}")

    def test_invalid_port_list(self):
        invalid_port_lists = [
            None,                   # not a list
            "80,443",                # wrong type
            80,                     # wrong type
            [],                     # optional: only if you disallow empty lists
            [0],                    # out of range
            [65536],                # out of range
            [-1],                   # negative
            [22, 70000],            # mixed invalid
            [22, "443"],            # wrong element type
            [True],                 # bool is not valid int
            [22, False],            # bool inside list
            [22.5],                 # float
            [[80, 443]],             # nested list
        ]

        for plist in invalid_port_lists:
            with self.assertRaises((TypeError, ValueError), msg=f"Failed on {plist}"):
                helper.validate_port_list(plist)


class TestParsePorts(unittest.TestCase):

    def test_valid_port_args(self):
        valid_ports_args = [
            "1",
            "22",
            "80",
            "443",
            "65535",
            "22,80,443",
            "65535,1,1024",
            "1-1",
            "1-10",
            "10-1",            # descending range
            "1024-1030",
            "65534-65535",
        ]

        port_lists = []

        for arg in valid_ports_args:
            port_list = helper.parse_ports(arg)
            self.assertIsInstance(port_list, list)
            port_lists.append(port_list)

        for port_list in port_lists:
            self.assertIsNone(helper.validate_port_list(port_list))

    def test_invalid_port_args(self):
        invalid_ports_args = [
            "",
            " ",
            "abc",
            "all",
            "22, 80",          # whitespace breaks regex
            "22,80,",          # trailing comma
            ",22,80",          # leading comma
            "22,,80",          # empty element
            "0",
            "-1",
            "65536",
            "0-10",
            "1-65536",
            "1-",
            "-10",
        ]

        for arg in invalid_ports_args:
            with self.assertRaises((ValueError, TypeError)):
                helper.parse_ports(arg)