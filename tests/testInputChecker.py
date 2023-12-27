import unittest
import input_checker


class TestChecker(unittest.TestCase):

    def testCheckParam(self):
        test1 = input_checker.check_param(5)
        test2 = input_checker.check_param(-1)
        self.assertEqual(True, test1)
        self.assertEqual(False, test2)

    def testCheckPort(self):
        test1 = input_checker.check_port(-1)
        test2 = input_checker.check_port(65)
        test3 = input_checker.check_port(1000000000000)
        self.assertEqual(False, test1)
        self.assertEqual(True, test2)
        self.assertEqual(False, test3)

    def testCheckIpv4WrongFormat(self):
        test = input_checker.check_ipv4("kjghsjklagalsk")
        self.assertEqual(False, test)

    def testCheckIpv4WrongOctetsNumber(self):
        test = input_checker.check_ipv4("1.1.1")
        self.assertEqual(False, test)

    def testCheckIpv4EmptyOctet(self):
        test = input_checker.check_ipv4("1.1..1")
        self.assertEqual(False, test)

    def testCheckIpv4WrongOctetNumber(self):
        test = input_checker.check_ipv4("1.1.256.1")
        test2 = input_checker.check_ipv4("1.1.-10.1")
        self.assertEqual(False, test)
        self.assertEqual(False, test2)

    def testCheckIpv4CorrectInput(self):
        test = input_checker.check_ipv4("1.1.1.1")
        self.assertEqual(True, test)

    def testIncorrectInput(self):
        error, res = input_checker.parse_ports(["90", "9o"])
        self.assertEqual(True, error)
        self.assertEqual(0, len(res))

    def testIncorrectRangeInput(self):
        error, res = input_checker.parse_ports(["90", "9o-100"])
        self.assertEqual(True, error)
        self.assertEqual(0, len(res))

    def testIncorrectRangeInputOrder(self):
        error, res = input_checker.parse_ports(["90-80"])
        self.assertEqual(False, error)
        self.assertEqual(0, len(res))

    def testCorrectSeveralPorts(self):
        error, res = input_checker.parse_ports(["80", "90"])
        self.assertEqual(False, error)
        self.assertEqual(2, len(res))
        self.assertSequenceEqual([80, 90], list(res))

    def testCorrectPortsRange(self):
        error, res = input_checker.parse_ports(["80-90"])
        self.assertEqual(False, error)
        self.assertEqual(11, len(res))
        self.assertSequenceEqual([x for x in range(80,91)], list(res))

    def testPortNotAppearTwice(self):
        error, res = input_checker.parse_ports(["80-85", "83"])
        self.assertEqual(False, error)
        self.assertEqual(6, len(res))
        self.assertSequenceEqual([x for x in range(80,86)], list(res))