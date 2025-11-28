from modules import port_scanner

target_host = "10.48.152.71"
target_ports = [21, 22, 80, 443]
timeout = 1
scanner = port_scanner.PortScanner(target_host, target_ports, timeout)

print("=== Port Scanner ===")
print("Target Host: " + target_host)

print("Target Ports:", end=" ")
for port in target_ports:
    print(str(port), end=" ")
print()

print("Timeout: " + str(timeout))

print("Starting TCP Scan")
for port in target_ports:
    result = scanner.tcp_scan(port)

    print(str(port) + " : " + str(result))