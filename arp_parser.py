import argparse


def get_args_parser():
    parser = argparse.ArgumentParser(prog="tcping",
                                     description='A CLI to portscan')
    parser.add_argument("--ping-timeout", type=float, default=2, help="set response timeout")
    parser.add_argument("-d", "--ping-delay", type=float, default=1, help="set delay between pings")
    parser.add_argument("-n", "--num-ping", type=int, default=4, help="set amount of pings")
    parser.add_argument("-i", "--inf-ping", action="store_true", help="set infinite ping")
    parser.add_argument("IP", type=str, help="set ip addr")
    parser.add_argument("-p", "--port", type=int, default=80, help="set port, default value is 80")
    return parser


