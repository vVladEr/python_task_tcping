import socket
import struct


def check_sum(head: list[int]):
    sum = 0
    for i in range(0, len(head)):
        sum = sum + (0xffff - head[i])

    sum = (sum >> 16) + (sum & 0xffff)
    return sum


def _parse_ipaddr_to_octets(ipaddr: str):
    return list(map(int, ipaddr.split(".")))


def create_ipheader(source_ip: str, dest_ip: str):
    ip_version = 4
    header_length = 5
    tos = 0
    total_length = 40  # ip_header + tcp_header
    id = 12345
    frag_off = 0
    ttl = 255
    protocol = socket.IPPROTO_TCP
    saddr = socket.inet_aton(source_ip)
    daddr = socket.inet_aton(dest_ip)
    s_octets = _parse_ipaddr_to_octets(source_ip)
    d_octets = _parse_ipaddr_to_octets(dest_ip)
    ip_headers = [((ip_version << 4) + header_length) << 8, total_length, id, (ttl << 8) + protocol,
                  (s_octets[0] << 8) + s_octets[1],
                  (s_octets[2] << 8) + s_octets[3],
                  (d_octets[0] << 8) + d_octets[1],
                  (d_octets[2] << 8) + d_octets[3]]
    checksum = check_sum(ip_headers)
    return struct.pack('!BBHHHBBH4s4s', (ip_version << 4) + header_length,
                       tos, total_length, id, frag_off, ttl, protocol, checksum,
                       saddr, daddr)


def create_packet(dest_ip: str, dest_port: str):
    local_ip = socket.gethostname()
    ip_address = socket.gethostbyname(local_ip)
    ip_header = create_ipheader(ip_address, dest_ip)
    print(struct.unpack("!BBHHHBBH4s4s", ip_header))

create_packet("1.1.1.1", "80")
