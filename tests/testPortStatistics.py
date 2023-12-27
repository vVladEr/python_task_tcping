from port_statistics import PortStatistics
import unittest


class TestPortStatistics(unittest.TestCase):

    def testUpdateNotReceivedResp(self):
        stat = PortStatistics("1.1.1.1", 80)
        stat.update_statistics()
        self.assertEqual(1, stat._sent_packs)
        self.assertEqual(0, stat._received_packs)
        self.assertEqual(0, len(stat._times))

    def testUpdateReceivedResp(self):
        stat = PortStatistics("1.1.1.1", 80)
        stat.update_statistics(response_received=True, time=80)
        self.assertEqual(1, stat._sent_packs)
        self.assertEqual(1, stat._received_packs)
        self.assertEqual(1, len(stat._times))
        self.assertEqual(80, stat._times[0])
