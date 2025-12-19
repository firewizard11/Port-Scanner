import argparse
from modules import helper
from modules import port_scanner

class CLI:

    def run(self):
        self.get_args()
        self.setup_scanner()
        self.run_scan()
        self.print_results()

    def run_scan(self):
        self.open_ports = []

        try:            
            if self.args["threaded"]:
                self.open_ports = self.scanner.concurrent_scan()
            else:
                self.open_ports = self.scanner.sequential_scan()
        except KeyboardInterrupt:
            print("Caught Ctrl+C, Exiting...")
            exit(130)

    def print_results(self):
        print("=== SCAN REPORT ===")
        print(f"Target Host: {self.args["host"]}")

        print(f"Found {len(self.open_ports)} open ports")
        for port in self.args["ports"]:
            if port in self.open_ports:
                print(f"{port} :: Open")

    def setup_scanner(self):
        self.scanner = port_scanner.PortScanner(
            self.args["host"],
            self.args["ports"],
            self.args["timeout"],
            self.args["max_probes"],
            self.args["verbose"]
        )

    def get_args(self):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("-h", "--host", required=True, help="Target Host to Scan (supports: IPv4, Hostnames)")
        parser.add_argument("-p", "--ports", required=True, help="Ports to Test (formats: single, comma-sep, start-end)")
        parser.add_argument("-t", "--timeout", type=float, default=0.5, help="How many seconds to wait for a port to respond")
        parser.add_argument("-mp", "--max_probes", type=int, default=1, help="The highest number of probes to use in concurrent scans (must use -T)")
        parser.add_argument("-v", "--verbose", action="store_true", help="Makes output verbose")
        parser.add_argument("-T", "--threaded", action="store_true", help="Makes scan concurrent")
        parser.add_argument("--help", action="help", help="Shows this help message")

        args = parser.parse_args()

        self.args = {
            "host": args.host,
            "ports": helper.parse_ports(args.ports),
            "timeout": args.timeout,
            "max_probes": args.max_probes,
            "verbose": args.verbose,
            "threaded": args.threaded
        }
