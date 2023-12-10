import socket
import struct
import scapy

SRC_IP = socket.gethostbyname(socket.gethostname())
SRC_PORT = 80


def calculate_checksum(data):
    s = 0
    if len(data) % 2:
        data += b'0'
    for i in range(0, len(data), 2):
        s += data[i + 1] + (data[i] << 8)
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    s = ~s & 0xffff
    return s


def _parse_ipaddr_to_octets(ipaddr: str):
    return list(map(int, ipaddr.split(".")))


def _create_ip_header(dest_ip: str):
    ip_version = 4
    header_length = 5
    tos = 0
    total_length = 40  # ip_header + tcp_header
    id = 12345
    flags = 0
    frag_off = 0
    ttl = 255
    protocol = socket.IPPROTO_TCP
    cksum = 0
    saddr = socket.inet_aton(SRC_IP)
    daddr = socket.inet_aton(dest_ip)
    first_pack = struct.pack('!BBHHHBBH4s4s', (ip_version << 4) + header_length,
                             tos, total_length, id, (flags << 13) + frag_off, ttl, protocol, cksum,
                             saddr, daddr)
    cksum = calculate_checksum(first_pack)
    return struct.pack('!BBHHHBBH4s4s', (ip_version << 4) + header_length,
                       tos, total_length, id, (flags << 13) + frag_off, ttl, protocol, cksum,
                       saddr, daddr)


def _create_tcp_header(dest_port: int, dest_ip: str):
    seq_num = 0
    ack_num = 0
    hl = 5
    syn = 1
    win_size = socket.htons(5840)
    chksum = 0
    urgp = 0
    flag_packet = syn << 1
    hl_reserve = hl << 4
    tcp_header = struct.pack("HHLLBBHHH", SRC_PORT, dest_port,
                             seq_num, ack_num,
                             hl_reserve, flag_packet, win_size,
                             chksum, urgp)
    ps_header = _create_pseudo_tcp_header(dest_ip, len_tcp_header=len(tcp_header))
    ps_header = tcp_header + ps_header
    chksum = calculate_checksum(ps_header)
    return struct.pack("HHLLBBHHH", SRC_PORT, dest_port,
                       seq_num, ack_num,
                       hl_reserve, flag_packet, win_size,
                       chksum, urgp)


def _create_pseudo_tcp_header(dest_ip: str, len_tcp_header: int):
    saddr = socket.inet_aton(SRC_IP)
    daddr = socket.inet_aton(dest_ip)
    zeros = 0
    proto = socket.IPPROTO_TCP
    return struct.pack("!4s4sBBH", saddr, daddr, zeros, proto, len_tcp_header)


def create_packet(dest_ip: str, dest_port: str):
    ip_header = _create_ip_header(dest_ip)
    tcp_header = _create_tcp_header(int(dest_port), dest_ip)
    return ip_header + tcp_header


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SRC_IP, SRC_PORT))
print("------------")
dest_ip = "1.1.1.1"
packet = create_packet(dest_ip, "80")
s.sendto(packet, (dest_ip, 80))
print("end")
