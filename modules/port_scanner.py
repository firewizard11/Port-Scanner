import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from modules import helper


MAX_PORT = 65535


class PortScanner():

    def __init__(self, target_host: str, target_ports: list[int], timeout: int = 1, max_probes: int = 1, verbose: bool = False):
        self.target_host = target_host

        self.target_ports = target_ports
        helper.validate_port_list(self.target_ports)
        
        self.timeout = timeout # The amount of time to wait before ending a probe
        if self.timeout < 1:
            raise ValueError("timeout should be greater than 0")
        
        self.max_probes = max_probes
        if self.max_probes < 1:
            raise ValueError("max_probes should be 1 or higher")
        
        self.verbose = verbose


    def sequential_scan(self) -> list[int]:
        """Scan each port in target_ports one after the other
        :returns:
        open_ports(list[int]): List of port numbers that returned True with the probe
        """
        if self.verbose: print(f"[*] Starting Sequential Scan on {self.target_host}")
        open_ports = []

        for port in self.target_ports:
            if self.verbose: print(f"[*] Scanning {port}")
            if self.tcp_probe(port): 
                if self.verbose: print(f"[+] {port} is Open")
                open_ports.append(port)

        return open_ports
    
    def concurrent_scan(self) -> list[int]:
        """Scan self.max_probes number of ports in target_ports till done
        :returns:
        open_ports(list[int]): List of port numbers that returned True with the probe
        """
        if self.verbose: print(f"[*] Starting Concurrent Scan on {self.target_host} (max_probes={self.max_probes})")
        open_ports = []

        with ThreadPoolExecutor(self.max_probes) as pool:
            futures = {pool.submit(self.tcp_probe, port):port for port in self.target_ports}

            for future in as_completed(futures):
                port = futures[future]
                if self.verbose: print(f"[*] Scanning {port}")
                is_open = future.result()
                
                if is_open:
                    if self.verbose: print(f"[+] {port} is Open")
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
