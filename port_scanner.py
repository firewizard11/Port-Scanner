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
    global open_ports
    open_ports = []

    print(f'[*] Starting Port Scan on host: {host}...')

    for port in ports:
        tcp_scan(host, port)
    
    print(f'[*] Port Scan Ended for host: {host}')


    print('=' * 100)

    if len(open_ports) > 0:
        for port in open_ports:
            print(f'[$] {port} | OPEN')
    else:
        print('[!] There are no OPEN ports')


def tcp_scan(host: str, port: int) -> None:
    # TODO: Check for filtered ports

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
        open_ports.append(port)


def cli() -> Tuple[str, List[int]]:
    # TODO: add a help section and improve the look and feel of cli
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
    # TODO: Validate port number range (0-65535)
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