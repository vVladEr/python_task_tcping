import random
import time
from scapy.layers.inet import IP, TCP, ICMP
from scapy.packet import Packet
from scapy.sendrecv import sr1
from port_statistics import PortStatistics


class TcPinger:
    def __init__(self, dst_ip, dst_ports, ping_timeout=2, ping_delay=1, ping_num=4, inf_ping=False):
        self._dst_ip = dst_ip
        self._src_port = random.randint(1025, 65534)
        self._dst_ports = dst_ports
        self._ping_timeout = ping_timeout
        self._ping_delay = ping_delay
        self._ping_num = ping_num
        self._inf_ping_flag = inf_ping
        self.statistics = dict()
        for port in dst_ports:
            self.statistics[port] = PortStatistics(dst_ip=dst_ip, dst_port=port)

    def _process_one_ping(self, dst_port: int):
        syn_packet = IP(dst=self._dst_ip) / TCP(sport=self._src_port, dport=dst_port, flags="S")
        start_time = time.perf_counter()
        resp_packet = sr1(syn_packet, timeout=self._ping_timeout, verbose=0)
        spent_time = time.perf_counter() - start_time
        spent_time = round(spent_time * 1000)
        self._parse_resp_packet(resp_packet=resp_packet, spent_time=spent_time, dst_port=dst_port)
        self._close_connection(dst_port)

    def _parse_resp_packet(self, resp_packet: Packet, spent_time: float, dst_port: int):
        is_received = False
        resp_time = -1
        if resp_packet is None:
            self._print_line(is_received=False, dst_port=dst_port)
        elif resp_packet.haslayer("TCP"):
            self._parse_tcp_resp_packet(resp_packet, spent_time, dst_port=dst_port)
            resp_time = spent_time
            is_received = True
        else:
            print("unexpected response without TCP layer")
        self.statistics[dst_port].update_statistics(is_received, time=resp_time)

    def _parse_tcp_resp_packet(self, packet: Packet, spent_time: float, dst_port: int):
        flag = packet.getlayer("TCP").flags
        if flag == 0x12:
            self._print_line(is_received=True, message="open",
                             ans_time=spent_time, dst_port=dst_port)
        elif flag == 0x14 or flag == 0x04:
            self._print_line(is_received=True, message="closed",
                             ans_time=spent_time, dst_port=dst_port)
        else:
            print(f"received unexpected flags combination in response packet: {hex(int(flag))}")

    def _close_connection(self, dst_port):
        sr1(IP(dst=self._dst_ip) / TCP(sport=self._src_port, dport=dst_port, flags='R'),
            timeout=1,
            verbose=0)

    def start_ping(self):
        print(f"start ping {self._dst_ip}:{self._dst_ports}:")
        if self._inf_ping_flag:
            while True:
                self._ping()
        else:
            for i in range(self._ping_num):
                self._ping()
        self.print_statistics()

    def _ping(self):
        for port in self._dst_ports:
            self._process_one_ping(dst_port=port)
            time.sleep(self._ping_delay)

    def _print_line(self, dst_port: int, is_received: bool, ans_time=0.0, message="", ):
        if is_received:
            print(f"{self._dst_ip}:{dst_port} is {message} time={ans_time} ms")
        else:
            print(f"No response from {self._dst_ip}:{dst_port}")

    def print_statistics(self):
        print("---------------------------------")
        for stat in self.statistics.values():
            print(stat)
            print("---------------------------------")
