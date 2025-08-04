import argparse
import re
import socket

from modules import scanner


def run():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("--help", action="help", help="Opens the Help Menu")
    parser.add_argument("--host", "-h", required=True, help="The Target Address")
    parser.add_argument(
        "--ports",
        "-p",
        required=True,
        help="Ports to Scan (Supported Formats: single port, start-end, comma-sep)",
    )
    parser.add_argument(
        "--threads", "-t", type=int, help="Max number of scans to perform at once"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Setting this will display closed ports",
    )

    args = parser.parse_args()

    host: str = args.host

    try:
        ports: list[int] = parse_ports(args.ports)
    except ValueError as e:
        print(e)
        return

    for port in ports:
        if not validate_port(port):
            print("Error: {} is not a valid port".format(port))
            return

    threads = args.threads
    if threads and threads < 1:
        print("Error: --threads should be greater than 0, not {}".format(threads))
        return

    verbose = args.verbose

    print("Testing {}:".format(host))
    pool = None

    try:
        if not threads:
            scanner.sequential_scan(host, ports, verbose)
        else:
            scanner.concurrent_scan(host, ports, threads, verbose)

    except KeyboardInterrupt:
        print("\nCaught Keyboard Interrupt: Exiting...")

        if pool:
            pool.shutdown(wait=False, cancel_futures=True)
    except socket.gaierror:
        print("Error: Invalid Address")

def parse_ports(ports: str) -> list[int]:
    re_dash = re.compile(r"^\d+-\d+$")
    re_csv = re.compile(r"^\d+(,\d+)*$")
    re_single = re.compile(r"^\d+$")

    if re_single.fullmatch(ports):
        return [int(ports)]

    if re_csv.fullmatch(ports):
        return list(map(int, ports.split(",")))

    if re_dash.fullmatch(ports):
        start = int(ports.split("-")[0])
        end = int(ports.split("-")[1])

        return list(range(start, end + 1))

    raise ValueError(
        "Error: ports {} is not in a valid format (e.g. number | start-end | number,number,...,number)".format(
            ports
        )
    )


def validate_port(port: int) -> bool:
    return 0 <= port <= 65535

