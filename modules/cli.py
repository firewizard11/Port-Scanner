import argparse
from modules import helper
from modules import port_scanner


def run() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--host", help="Target Host to Scan (supports: IPv4, Hostnames)")
    parser.add_argument("-p", "--ports", help="Ports to Test (formats: single, comma-sep, start-end)")
    parser.add_argument("-t", "--timeout", type=float, default=0.5, help="How many seconds to wait for a port to respond")
    parser.add_argument("-mp", "--max_probes", type=int, default=1, help="The highest number of probes to use in concurrent scans (must use -T)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Makes output verbose")
    parser.add_argument("-T", "--threaded", action="store_true", help="Makes scan concurrent")
    parser.add_argument("--help", action="help", help="Shows this help message")

    args = parser.parse_args()

    if None in (args.host, args.ports):
        parser.print_help()
        return 0

    arg_list = {
        "host": args.host,
        "ports": helper.parse_ports(args.ports),
        "timeout": args.timeout,
        "max_probes": args.max_probes,
        "verbose": args.verbose,
        "threaded": args.threaded
    }

    scanner = port_scanner.PortScanner(
        arg_list["host"],
        arg_list["ports"],
        arg_list["timeout"],
        arg_list["max_probes"],
        arg_list["verbose"]
    )

    open_ports = []

    try:            
        if arg_list["threaded"]:
            open_ports = scanner.concurrent_scan()
        else:
            open_ports = scanner.sequential_scan()
    except KeyboardInterrupt:
        print("Caught Ctrl+C, Exiting...")
        return 130

    print("=== SCAN REPORT ===")
    print(f"Target Host: {arg_list["host"]}")

    print(f"Found {len(open_ports)} open ports")
    for port in arg_list["ports"]:
        if port in open_ports:
            print(f"{port} :: Open")

    return 0
