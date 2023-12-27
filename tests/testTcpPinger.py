import unittest
import unittest.mock
import io
from scapy.layers.inet import IP, TCP

from tcp_pinger import TcPinger


class TestTcPinger(unittest.TestCase):
    def setUp(self):
        self.tcpPinger = TcPinger("1.1.1.1", [80])

    def test_parse_none_resp_packet(self):
        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.tcpPinger._parse_resp_packet(resp_packet=None, spent_time=0, dst_port=80)
            self.assertEqual(fake_out.getvalue(), f"No response from {self.tcpPinger._dst_ip}:{80}\n")

    def test_parse_not_tcp_resp_packet(self):
        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            packet = IP(dst=self.tcpPinger._dst_ip)
            self.tcpPinger._parse_resp_packet(resp_packet=packet, spent_time=0, dst_port=80)
            self.assertEqual(fake_out.getvalue(), f"unexpected response without TCP layer\n")

    def test_parse_syn_ack_tcp_resp_packet(self):
        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            packet = IP(dst=self.tcpPinger._dst_ip) / TCP(sport=1234, dport=80, flags="SA")
            self.tcpPinger._parse_resp_packet(resp_packet=packet, spent_time=0, dst_port=80)
            self.assertEqual(fake_out.getvalue(), f"1.1.1.1:80 is open time=0 ms\n")

    def test_parse_rst_tcp_resp_packet(self):
        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            packet = IP(dst=self.tcpPinger._dst_ip) / TCP(sport=1234, dport=80, flags="R")
            self.tcpPinger._parse_resp_packet(resp_packet=packet, spent_time=0, dst_port=80)
            self.assertEqual(fake_out.getvalue(), f"1.1.1.1:80 is closed time=0 ms\n")

    def test_parse_unexpected_flags_tcp_resp_packet(self):
        with unittest.mock.patch('sys.stdout', new=io.StringIO()) as fake_out:
            packet = IP(dst=self.tcpPinger._dst_ip) / TCP(sport=1234, dport=80, flags="A")
            self.tcpPinger._parse_resp_packet(resp_packet=packet, spent_time=0, dst_port=80)
            self.assertEqual(fake_out.getvalue(), "received unexpected flags combination in response packet: 0x10\n")
