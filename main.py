import logging
from arp_parser import get_args_parser
from tcp_pinger import TcPinger
from input_checker import  check_input

#logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

parser = get_args_parser()
args = parser.parse_args()
if check_input(args):
    pinger = TcPinger(args.IP, args.port, args.ping_timeout,
                      args.ping_delay, args.num_ping, args.inf_ping)
    try:
        pinger.start_ping()
    except KeyboardInterrupt as e:
        pinger.print_statistics()
