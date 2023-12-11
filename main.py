import logging
from packet_constructor import TcPinger

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
pinger = TcPinger("1.1.1.1")
pinger.start_ping()
