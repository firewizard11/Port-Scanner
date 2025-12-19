from re import fullmatch

MAX_PORT = 65535
MIN_PORT = 1


def validate_port_list(port_list: list[int]):
    """Validates a list of port numbers
    :raises:
    - TypeError
    - ValueError
    """

    if not isinstance(port_list, list):
        raise TypeError("portlist should be a list")

    if len(port_list) < 1:
        raise ValueError(
            f"portlist should have atleast 1 port (current={len(port_list)})"
        )

    if len(port_list) > MAX_PORT:
        raise ValueError(
            f"portlist should have less than 65535 ports (current={len(port_list)})"
        )

    for port in port_list:
        validate_port(port)


def validate_port(port: int):
    """Validates a port number
    :raises:
    - TypeError
    - ValueError
    """
    if not isinstance(port, int) or isinstance(port, bool):
        raise TypeError("port should be of type int")

    if not (MIN_PORT <= port <= MAX_PORT):
        raise ValueError("port should be between 1 and 65535 (inclusive)")


def parse_ports(ports_arg: str) -> list[int]:
    r_single = r"\d{1,5}"
    r_csv = r"\d{1,5}(,\d{1,5})*"
    r_range = r"\d{1,5}-\d{1,5}"
    ports_list = []

    if fullmatch(r_single, ports_arg):
        ports_list.append(int(ports_arg))
    elif fullmatch(r_csv, ports_arg):
        ports_str = ports_arg.split(",")
        for port in ports_str:
            ports_list.append(int(port))
    elif fullmatch(r_range, ports_arg):
        start, end = ports_arg.split("-")
        start, end = int(start), int(end)

        if start < end:
            for port in range(start, end + 1):
                ports_list.append(port)
        elif start == end:
            ports_list.append(start)
        else:
            for port in range(start, end - 1, -1):
                ports_list.append(port)

    try:
        validate_port_list(ports_list)
    except Exception as e:
        print("Please enter a valid port or port list")
        raise e

    return ports_list
