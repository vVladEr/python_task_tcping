import socket
import struct
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1, srp1

SRC_IP = socket.gethostbyname(socket.gethostname())
SRC_PORT = 1030


def syn_scan(ip, port):  # В данном месте проводится сканирование путем отправки пакетов
    syn_packet = IP(dst=ip) / TCP(dport=port, flags="S")  # Флаг S означает SYN пакет
    resp_packet = srp1(syn_packet, timeout=2)  # Время ожидания пакета можно ставить свое
    if resp_packet is not None:
        if resp_packet.getlayer('TCP').flags & 0x12 != 0:
            print(f"{ip}:{port} is open/{resp_packet.sprintf('%TCP.sport%')}")


syn_scan("1.1.1.1", 80)
