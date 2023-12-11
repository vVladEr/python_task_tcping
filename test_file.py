import random
import socket
import logging


from scapy.layers.inet import IP, TCP, ICMP
from scapy.layers.l2 import getmacbyip
from scapy.sendrecv import sr1, sr


logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
print(getmacbyip(socket.gethostbyname(socket.gethostname())))
host = "1.1.1.1"
port_range = [22, 23, 80, 443, 3389]

# Send SYN with random Src Port for each Dst port
for dst_port in port_range:
    src_port = random.randint(1025, 65534)
    resp = sr1(
        IP(dst=host) / TCP(sport=src_port, dport=dst_port, flags="S"), timeout=1,
        verbose=0
    )

    if resp is None:
        print(f"{host}:{dst_port} is filtered (silently dropped).")

    elif resp.haslayer(TCP):
        if resp.getlayer(TCP).flags == 0x12:
            # Send a gratuitous RST to close the connection
            send_rst = sr(
                IP(dst=host) / TCP(sport=src_port, dport=dst_port, flags='R'),
                timeout=1,
                verbose=0,
            )
            print(f"{host}:{dst_port} is open.")

        elif resp.getlayer(TCP).flags == 0x14:
            print(f"{host}:{dst_port} is closed.")

    elif resp.haslayer(ICMP):
        if (
                int(resp.getlayer(ICMP).type) == 3 and
                int(resp.getlayer(ICMP).code) in [1, 2, 3, 9, 10, 13]
        ):
            print(f"{host}:{dst_port} is filtered (silently dropped).")
