"""WARNING: TESTS CAN GET SLOW"""
import random
import socket
import unittest
from modules import port_scanner

def create_port(port: int, open: bool) -> socket:
    addr = ("localhost", port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    s.bind(addr)
    if open: s.listen(2)
    return s


class TestPortScanner(unittest.TestCase):

    def setUp(self):

        self.port_list = []
        for _ in range(20):
            self.port_list.append(random.randrange(30000, 65536))

        self.scanner = port_scanner.PortScanner("localhost", self.port_list, timeout=0.1)
        self.port_dict = {}
        
        for port in self.port_list:
            self.port_dict[port] = None

    def tearDown(self):
        for port in self.port_list:
            if type(self.port_dict[port]) is socket.socket: self.port_dict[port].close()

    def create_ports(self, open: bool):
        for port in self.port_list:
            try:
                self.port_dict[port] = create_port(port, open)
            except PermissionError:
                self.port_list.remove(port)

class TestTCPProbe(TestPortScanner):

    def test_open_ports(self):
        self.create_ports(True)
        for port in self.port_list:
            self.assertTrue(self.scanner.tcp_probe(port))

    def test_closed_ports(self):
        self.create_ports(False)
        for port in self.port_list:
            self.assertFalse(self.scanner.tcp_probe(port))

class TestSequentialScan(TestPortScanner):
    
    def test_open_ports(self):
        self.create_ports(True)
        result_list = self.scanner.sequential_scan()
        self.assertEqual(self.port_list, result_list)

    def test_closed_ports(self):
        self.create_ports(False)
        result_list = self.scanner.sequential_scan()
        self.assertEqual([], result_list)