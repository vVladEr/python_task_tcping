def check_ipv4(ipv4: str) -> bool:
    try:
        octets = list(map(int, ipv4.split(".")))
        if len(octets) != 4:
            return False
        else:
            for octet in octets:
                if octet > 255 or octet < 0:
                    return False
            return True
    except ValueError:
        return False


def check_port(port: int) -> bool:
    return 0 <= port <= 65535


def check_param(param: int) -> bool:
    return param >= 0


def check_input(args):
    if not check_ipv4(args.IP):
        print("Wrong IP addr format")
        return False
    if not check_port(args.port):
        print("Wrong port argument")
        return False
    if not check_param(args.ping_timeout):
        print("Wrong ping timeout argument")
        return False
    if not check_param(args.ping_delay):
        print("Wrong ping delay argument")
        return False
    if not check_param(args.num_ping):
        print("Wrong amount of pings argument")
        return False
    return True
