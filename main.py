from modules import port_scanner

target_host = "10.48.161.248"
target_ports = list(range(1,65535+1))
timeout = 1
max_probes = 200
scanner = port_scanner.PortScanner(target_host, target_ports, timeout, max_probes)

print("=== Port Scanner ===")
print(f"[*] Scanning {target_host}")
open_ports = scanner.concurrent_scan()
print()

print("Results:")
for port in target_ports:
    print(f"{port} || {"Open" if port in open_ports else "Closed"}")
