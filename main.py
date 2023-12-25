from arp_parser import get_args_parser
from tcp_pinger import TcPinger
from input_checker import check_input, parse_watchdog_ports


parser = get_args_parser()
args = parser.parse_args()
ports = []
break_flag = False
if args.watchdog is not None:
    error, ports = parse_watchdog_ports(args.watchdog)
    args.inf_ping = True
    if error:
        print("Wrong watchdog ports format")
        exit()

if check_input(args):
    if len(ports) == 0:
        ports = [args.port]
    pinger = TcPinger(args.IP, ports, args.ping_timeout,
                      args.ping_delay, args.num_ping, args.inf_ping)
    try:
        pinger.start_ping()
    except KeyboardInterrupt as e:
        pinger.print_statistics()
