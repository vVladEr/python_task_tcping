from arg_parser import get_args_parser
from tcp_pinger import TcPinger
from input_checker import check_input, parse_ports


parser = get_args_parser()
args = parser.parse_args()

if check_input(args):
    error, ports = parse_ports(args.ports)
    if error:
        print("Wrong ports format")
        exit()
    if args.watchdog:
        args.inf_ping = True
    pinger = TcPinger(args.IP, ports, args.ping_timeout,
                      args.ping_delay, args.num_ping, args.inf_ping)
    try:
        pinger.start_ping()
    except KeyboardInterrupt as e:
        pinger.print_statistics()
