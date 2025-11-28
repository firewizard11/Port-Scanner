from modules import port_scanner

target_host = "10.48.161.248"
target_ports = list(range(1,65535+1))
timeout = 1
max_probes = 200
scanner = port_scanner.PortScanner(target_host, target_ports, timeout)

print("=== Port Scanner ===")
print("Target Host: " + target_host)

print("Target Ports:", end=" ")
for port in target_ports:
    print(str(port), end=" ")
print()

print("Timeout: " + str(timeout))

print("Starting TCP Scan")
open_ports = scanner.concurrent_scan()

print("Results:")
for port in target_ports:
    print(f"{port} || {"Open" if port in open_ports else "Closed"}")
