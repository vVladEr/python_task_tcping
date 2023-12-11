import random
import time

from scapy.layers.inet import IP, TCP, ICMP
from scapy.sendrecv import sr1, sr


class TcPinger:
    def __init__(self, dst_ip, dst_port=80, ping_timeout=2, ping_delay=1, ping_num=4, inf_ping=False):
        self._dst_ip = dst_ip
        self._src_port = random.randint(1025, 65534)
        self._dst_port = dst_port
        self._ping_timeout = ping_timeout
        self._ping_delay = ping_delay
        self._ping_num = ping_num
        self._inf_ping_flag = inf_ping
        self._received_packs = 0
        self._times = []

    def ping(self):
        syn_packet = IP(dst=self._dst_ip) / TCP(sport=self._src_port, dport=self._dst_port, flags="S")
        start_time = time.perf_counter()
        resp_packet = sr1(syn_packet, timeout=self._ping_timeout, verbose=0)
        spent_time = time.perf_counter() - start_time
        if resp_packet is None:
            self.print_line(is_received=False)
        elif resp_packet.haslayer("TCP"):
            if resp_packet.getlayer("TCP").flags & 0x12 != 0:
                _ = sr(IP(dst=self._dst_ip) / TCP(sport=self._src_port, dport=self._dst_port, flags='R'),
                       timeout=1,
                       verbose=0)
                self.print_line(is_received=True, message="open", ans_time=spent_time)

            elif resp_packet.getlayer("TCP").flags & 0x14:
                self.print_line(is_received=True, message="close", ans_time=spent_time)
            self._times.append(spent_time)
            self._received_packs += 1
        elif resp_packet.haslayer(ICMP):
            if int(resp_packet.getlayer(ICMP).type) == 3:
                self.print_line(is_received=False)

    def start_ping(self):
        if self._inf_ping_flag:
            while True:
                self.ping()
                time.sleep(self._ping_delay)
        else:
            for i in range(self._ping_num):
                self.ping()
                time.sleep(self._ping_delay)

    def print_line(self, is_received, ans_time=0.0, message=""):
        if is_received:
            print(f"{self._dst_ip}:{self._dst_port} is {message} time={round(ans_time * 1000)} ms")
        else:
            print(f"No response from {self._dst_ip}:{self._dst_port}")
