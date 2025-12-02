import argparse
import re
import helper

class CLI:

    def run(self):
        pass

    def setup(self):
        pass

    def get_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--host", required=True)
        parser.add_argument("--ports", required=True)
        parser.add_argument("--timeout", type=int, default=1)
        parser.add_argument("--max_probes", type=int, default=0)
        parser.add_argument("--verbose", type=bool, default=False)

        args = parser.parse_args()
        
        print(args)


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