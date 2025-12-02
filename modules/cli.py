import argparse
import re
from modules import helper
from modules import port_scanner

class CLI:

    def run(self):
        self.get_args()
        self.setup_scanner()

    def print_results(self):
        pass

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
        parser.add_argument("-h", "--host", required=True)
        parser.add_argument("-p", "--ports", required=True)
        parser.add_argument("-t", "--timeout", type=int, default=1)
        parser.add_argument("-mp", "--max_probes", type=int, default=1)
        parser.add_argument("-v", "--verbose", type=bool, default=False)
        parser.add_argument("-st", "--scan_type", choices=[
            "tcp",
        ], required=True)

        args = parser.parse_args()

        self.args = {
            "host": args.host,
            "ports": self.parse_ports(args.ports),
            "timeout": args.timeout,
            "max_probes": args.max_probes,
            "verbose": args.verbose,
            "scan_type": args.scan_type
        }

    def parse_ports(self, ports_arg: str) -> list[int]:
        r_single = r"\d{1,5}"
        r_csv = r"(\d{1,5},{0,1})+"
        r_range = r"\d{1,5}-\d{1,5}"
        ports_list = []

        if re.fullmatch(r_single, ports_arg):
            ports_list.append(int(ports_arg))
        elif re.fullmatch(r_csv, ports_arg):
            ports_str = ports_arg.split(",")
            for port in ports_str:
                ports_list.append(int(port))
        elif re.fullmatch(r_range, ports_arg):
            start, end = ports_arg.split("-")
            for port in range(int(start), int(end) + 1):
                ports_list.append(port)
        
        try:
            helper.validate_port_list(ports_list)
        except:
            print("Please enter a valid port or port list")
            exit(1)
        
        return ports_list