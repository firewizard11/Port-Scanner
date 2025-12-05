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
        raise ValueError(f"portlist should have atleast 1 port (current={len(port_list)})")
    
    if len(port_list) > 65535:
        raise ValueError(f"portlist should have less than 65535 ports (current={len(port_list)})")
    
    for port in port_list:
        validate_port(port)

def validate_port(port: int):
    """Validates a port number
    :raises:
    - TypeError
    - ValueError
    """
    if not isinstance(port, int):
        raise TypeError("port should be of type int")
    
    if not (0 < port <= 65535):
        raise ValueError("port should be between 1 and 65535 (inclusive)")