import logging
from  arp_parser import get_args_parser
from tcp_pinger import TcPinger

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

parser = get_args_parser()
args = parser.parse_args()

pinger = TcPinger(args.IP, args.port, args.ping_timeout,
                  args.ping_delay, args.num_ping, args.inf_ping)
try:
    pinger.start_ping()
except KeyboardInterrupt as e:
    pinger.print_statistics()
