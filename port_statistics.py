from statistics import mean


class PortStatistics:
    def __init__(self, dst_ip: str, dst_port: int):
        self._dst_ip = dst_ip
        self._dst_port = dst_port
        self._received_packs = 0
        self._sent_packs = 0
        self._times = []

    def __str__(self):
        loss_percent = ((self._sent_packs - self._received_packs) / self._sent_packs) * 100
        line = (f"Statistics for {self._dst_ip}:{self._dst_port}:\n"
                f"\tPackets: Sent = {self._sent_packs}, Received = {self._received_packs},"
                f" Lost = {self._sent_packs - self._received_packs}\n"
                f"\t({round(loss_percent, 3)}% losses)")
        if len(self._times):
            time_line = (f"\nSend-receive time in ms:\n"
                         f"\tMin = {min(self._times)}, Max = {max(self._times)}, Avg = {round(mean(self._times), 3)}")
            line += time_line
        return line

    def update_statistics(self, response_received=False, time: float = None):
        self._sent_packs += 1
        if response_received:
            self._received_packs += 1
            self._times.append(time)
