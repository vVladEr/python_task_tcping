from statistics import mean


class PortStatistics:
    def __init__(self, dst_ip: str, dst_port: int):
        self._dst_ip = dst_ip
        self._dst_port = dst_port
        self.received_packs = 0
        self.sent_packs = 0
        self.times = []

    def __str__(self):
        loss_percent = ((self.sent_packs - self.received_packs) / self.sent_packs) * 100
        line = (f"Statistics for {self._dst_ip}:{self._dst_port}:\n"
                f"\tPackets: Sent = {self.sent_packs}, Received = {self.received_packs},"
                f" Lost = {self.sent_packs - self.received_packs}\n"
                f"\t({round(loss_percent, 3)}% losses)")
        if len(self.times):
            time_line = (f"\nSend-receive time in ms:\n"
                         f"\tMin = {min(self.times)}, Max = {max(self.times)}, Avg = {round(mean(self.times), 3)}")
            line += time_line
        return line
