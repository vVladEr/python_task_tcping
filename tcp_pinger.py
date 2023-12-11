import random
import time
from statistics import mean
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
        self._sent_packs = 0
        self._times = []

    def _ping(self):
        syn_packet = IP(dst=self._dst_ip) / TCP(sport=self._src_port, dport=self._dst_port, flags="S")
        start_time = time.perf_counter()
        resp_packet = sr1(syn_packet, timeout=self._ping_timeout, verbose=0)
        spent_time = time.perf_counter() - start_time
        spent_time = round(spent_time * 1000)
        if resp_packet is None:
            self._print_line(is_received=False)
        elif resp_packet.haslayer("TCP"):
            if resp_packet.getlayer("TCP").flags & 0x12 != 0:
                _ = sr(IP(dst=self._dst_ip) / TCP(sport=self._src_port, dport=self._dst_port, flags='R'),
                       timeout=1,
                       verbose=0)
                self._print_line(is_received=True, message="open", ans_time=spent_time)

            elif resp_packet.getlayer("TCP").flags & 0x14:
                self._print_line(is_received=True, message="close", ans_time=spent_time)
            self._times.append(spent_time)
            self._received_packs += 1
        elif resp_packet.haslayer(ICMP):
            if int(resp_packet.getlayer(ICMP).type) == 3:
                self._print_line(is_received=False)

    def start_ping(self):
        if self._inf_ping_flag:
            while True:
                self._ping()
                self._sent_packs += 1
                time.sleep(self._ping_delay)
        else:
            for i in range(self._ping_num):
                self._ping()
                self._sent_packs += 1
                time.sleep(self._ping_delay)
        self.print_statistics()

    def _print_line(self, is_received, ans_time=0.0, message=""):
        if is_received:
            print(f"{self._dst_ip}:{self._dst_port} is {message} time={ans_time} ms")
        else:
            print(f"No response from {self._dst_ip}:{self._dst_port}")

    def print_statistics(self):
        print(f"Statistics for {self._dst_ip}:{self._dst_port}:")
        print(f"\tPackets: Sent = {self._sent_packs}, Received = {self._received_packs},"
              f" Lost = {self._sent_packs - self._received_packs}")
        loss_percent = ((self._sent_packs - self._received_packs) / self._sent_packs) * 100
        print(f"\t({round(loss_percent, 3)}% losses)")
        if len(self._times):
            print(f"Send-receive time in ms:")
            print(f"\tMin = {min(self._times)}, Max = {max(self._times)}, Avg = {round(mean(self._times), 3)}")
