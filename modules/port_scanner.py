import socket


MAX_PORT = 65535


class PortScanner():

    def __init__(self, target_host: str, target_ports: list[int], timeout: int):
        self.target_host = target_host
        self.target_ports = target_ports
        self.timeout = timeout

    def tcp_scan(self, target_port: int) -> bool:
        target_addr = (self.target_host, target_port)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(self.timeout)
            try:
                sock.connect(target_addr)
                return True
            except:
                return False