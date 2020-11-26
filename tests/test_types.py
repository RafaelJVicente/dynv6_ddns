import unittest

from dynv6_ddns.types import Token, IPv4


class TestTypes(unittest.TestCase):
    def test_token(self):
        token = Token("1234567890")
        self.assertIsInstance(token, str, "Should be str")

    def test_ipv4(self):
        ip = IPv4("8.8.8.8")
        self.assertIsInstance(ip, str, "Should be str")


if __name__ == '__main__':
    unittest.main()
