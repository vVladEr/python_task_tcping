import argparse


def get_args_parser():
    parser = argparse.ArgumentParser(prog="tcping",
                                     description='A CLI to portscan')
    group = parser.add_mutually_exclusive_group(required=False)
    parser.add_argument("-t", "--ping-timeout", type=float, default=2, help="set response timeout")
    parser.add_argument("-d", "--ping-delay", type=float, default=1, help="set delay between pings")
    group.add_argument("-n", "--num-ping", type=int, default=4, help="set amount of pings")
    group.add_argument("-i", "--inf-ping", action="store_true", help="set infinite ping")
    parser.add_argument("IP", type=str, help="set ip addr")
    parser.add_argument("-p", "--port", type=int, default=80, help="set port, default value is 80")
    group.add_argument("-w", "--watchdog", nargs="*",  type=str, help="set ports to watchdog as [PORT|PORT-PORT]")
    return parser



