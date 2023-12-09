import argparse


def get_args_parser():
    parser = argparse.ArgumentParser(prog="tcping",
                                     description='A CLI to portscan')
    parser.add_argument("--ping-timeout", type=float, default=2)
    parser.add_argument("-d", "--ping-delay", type=float, default=0)
    parser.add_argument("-n", "--num-ping", type=int, default=3)
    parser.add_argument("-i", "--inf-ping", action="store_true")
    parser.add_argument("IP", type=str)
    parser.add_argument("port", type=int, default=80)
    return parser


