import argparse
from socket import socket, AF_INET, SOCK_STREAM
from typing import Tuple, List

banner = \
"""
  _____           _      _____                                 
 |  __ \         | |    / ____|                                
 | |__) |__  _ __| |_  | (___   ___ __ _ _ __  _ __   ___ _ __ 
 |  ___/ _ \| '__| __|  \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 | |  | (_) | |  | |_   ____) | (_| (_| | | | | | | |  __/ |   
 |_|   \___/|_|   \__| |_____/ \___\__,_|_| |_|_| |_|\___|_|   
"""


def main():
    print(banner)
    print('=' * 100)

    host, ports = cli()

    print(f'[*] Starting Port Scan on host: {host}...')

    for port in ports:
        scan_port(host, port)
    
    print(f'[*] Port Scan Ended for host: {host}')


def scan_port(host: str, port: int) -> None:
    with socket(AF_INET, SOCK_STREAM) as sock:
        print(f'[*] Testing port: {port}')
        sock.settimeout(1)
        
        try:
            sock.connect((host, port))
        except ConnectionRefusedError:
            print(f'[!] Connection Refused for port: {port}')
            return
        except TimeoutError:
            print(f'[!] Connection Timed out for port: {port}')
            return
        
        print(f'[*] Connected to port: {port}')


def cli() -> Tuple[str, List[int]]:
    parser = argparse.ArgumentParser(prog='Port Scanner', usage='python3 port_scanner.py host ports')

    parser.add_argument('host')
    parser.add_argument('ports')

    args = parser.parse_args()
    host: str =  args.host
    octets = host.split('.', 3)
    for octet in octets:
        if not octet.isnumeric() or not (0 <= int(octet) <= 255):
            raise ValueError(f'{host} is not an IPv4 address')

    ports: str = args.ports
    if ',' not in ports and '-' not in ports:
        try:
            ports = [int(ports)]
        except TypeError:
            raise ValueError(f'{ports} is not a port')
    elif ',' in ports:
        try:
            ports = [int(port) for port in ports.split(',')]
        except:
            raise ValueError(f'{ports} is not a port')
    elif '-' in ports:
        try:
            ports = list(range(int(ports.split('-', 1)[0]), int(ports.split('-', 1)[1]) + 1))
        except:
            raise ValueError(f'{ports} is not a port')

    return host, ports

main()