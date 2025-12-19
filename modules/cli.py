from argparse import ArgumentParser
from modules import helper
from modules import port_scanner

banner = \
"""
  _____           _      _____                                 
 |  __ \         | |    / ____|                                
 | |__) |__  _ __| |_  | (___   ___ __ _ _ __  _ __   ___ _ __ 
 |  ___/ _ \| '__| __|  \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 | |  | (_) | |  | |_   ____) | (_| (_| | | | | | | |  __/ |   
 |_|   \___/|_|   \__| |_____/ \___\__,_|_| |_|_| |_|\___|_|                                                                                                                                                                                                                                        
"""

def custom_help(parser: ArgumentParser):
    print(banner)
    parser.print_help()

def run() -> int:
    """Runs the port scanner program
    Returns:
      - int: Program return code on exit
        - 0: Exitted Normally
        - 1: Exitted w/ Error
        - 130: Exitted with Ctrl+C
    """

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "-h", "--host", help="Target Host to Scan (supports: IPv4, Hostnames), Required"
    )
    parser.add_argument(
        "-p",
        "--ports",
        help="Ports to Test (formats: single, comma-sep, start-end), Required",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=0.5,
        help="How many seconds to wait for a port to respond (default: 0.5s)",
    )
    parser.add_argument(
        "-mp",
        "--max_probes",
        type=int,
        default=1,
        help="Makes scan concurrent with MAX_PROBES as the number of max probes (default: 1 probe)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Makes output verbose"
    )
    parser.add_argument("--help", action="store_true", help="Shows this help message")

    args = parser.parse_args()

    if args.help or (None in (args.host, args.ports)):
        custom_help(parser)
        return 0

    try:
        parsed_ports = helper.parse_ports(args.ports)
    except Exception as e:
        print(e)  # Lazy
        return 1

    if args.max_probes < 0:
        print("Please enter max_probes greater than 1")
        return 1

    arg_list = {
        "host": args.host,
        "ports": parsed_ports,
        "timeout": args.timeout,
        "max_probes": args.max_probes,
        "verbose": args.verbose,
    }

    scanner = port_scanner.PortScanner(
        arg_list["host"],
        arg_list["ports"],
        arg_list["timeout"],
        arg_list["max_probes"],
        arg_list["verbose"],
    )

    open_ports = []

    try:
        if arg_list["max_probes"] > 1:
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
