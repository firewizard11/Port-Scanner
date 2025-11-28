import socket


MAX_PORT = 65535


class PortScanner():

    def __init__(self, target_host: str, target_ports: list[int], timeout: int):
        self.target_host = target_host
        self.target_ports = target_ports
        self.timeout = timeout # The amount of time to wait before ending a probe

    def sequential_scan(self) -> list[int]:
        """Scan each port in target_ports one after the other
        :returns:
        open_ports(list[int]): List of port numbers that returned True with the probe
        """
        open_ports = []

        for port in self.target_ports:
            if self.tcp_probe(port):
                open_ports.append(port)

        return open_ports

    def tcp_probe(self, target_port: int) -> bool:
        """ Completes full 3 way handshake to test port
        :args:
        target_port(int): The specific port number to test

        :returns:
        Probe Result(bool): The result of the scan
        - True = open
        - False = closed (not open)
        """
        target_addr = (self.target_host, target_port)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(self.timeout)
            try:
                sock.connect(target_addr)
                return True
            except:
                return False
    
    def validate_port(self, port: int):
        if not isinstance(port, int):
            raise TypeError("port should be of type int")
        
        if not (0 < port <= 65535):
            raise ValueError("port should be between 1 and 65535 (inclusive)")