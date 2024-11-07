from socket import socket, AF_INET, SOCK_STREAM


def main():
    host = '192.168.60.128'
    ports = [4444]

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

main()