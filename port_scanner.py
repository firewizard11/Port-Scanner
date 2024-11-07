import argparse
from socket import socket, AF_INET, SOCK_STREAM
from typing import Tuple, List


def main():
    host, ports = cli()

    print(f'[*] Starting Scan on host: {host}...')
    for port in ports:
        scan_port(host, port)


def scan_port(host: str, port: int) -> None:
    with socket(AF_INET, SOCK_STREAM) as sock:
        print(f'[*] Testing port: {port}')
        sock.settimeout(1)
        
        try:
            sock.connect((host, port))
        except ConnectionRefusedError:
            print(f'[!] Connection Refused on port: {port}')
            return
        except TimeoutError:
            print(f'[!] Connection Timed out on port: {port}')
            return
        
        print(f'[*] Connected to port: {port}')


def cli() -> Tuple[str, List[int]]:
    parser = argparse.ArgumentParser(prog='Port Scanner', usage='python3 port_scanner.py host ports')

    parser.add_argument('host')
    parser.add_argument('ports')

    args = parser.parse_args()
    host = args.host
    ports = args.ports

    

main()