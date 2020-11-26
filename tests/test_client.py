import json
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

from dynv6_ddns.client import Cli


class TestCli(unittest.TestCase):
    __file_path = Path("test_dynv6_ddns.json")
    __test_token = "5Y5tbDMg4g_ctb7sJpW-icuy1_hSZN"
    __test_ip = "8.8.8.8"

    def test_update_ipv4(self):
        self.__clean()

        client = Cli(self.__file_path, self.__test_token)
        client.update_ipv4()

        url = "https://dynv6.com/api/v2/zones"
        headers = {"Authorization": "Bearer {}".format(self.__test_token), "Accept": "application/json"}
        new_ip = requests.get(url=url, headers=headers).json()[0]["ipv4address"]

        # Reset dummy
        client = Cli(self.__file_path, self.__test_token, ipv4=self.__test_ip)
        client.update_ipv4()

        self.assertNotEqual(new_ip, self.__test_ip, "Should be {}".format(self.__test_ip))

        self.__clean()

    def test_get_current_public_ipv4(self):
        self.__clean()

        ipv4 = requests.get('https://checkip.amazonaws.com').text.strip()
        client = Cli(self.__file_path, self.__test_token)
        self.assertEqual(client.__dict__["_Cli__ipv4"], ipv4, "Should be {}".format(ipv4))

        self.__clean()

    def test_check_token(self):
        self.__clean()
        with self.assertRaises(ValueError):
            _ = Cli(self.__file_path, self.__test_token[:-1], "8.8.8.8")

        with patch('dynv6_ddns.client.requests.get') as mock_get:
            response = requests.Response()
            response.status_code = 404
            mock_get.return_value = response
            with self.assertRaises(requests.HTTPError):
                _ = Cli(self.__file_path, self.__test_token, "8.8.8.8")

        _ = Cli(self.__file_path, self.__test_token, "8.8.8.8")

        self.__clean()

    def test_check_ipv4(self):
        self.__clean()

        with self.assertRaises(SyntaxError):
            _ = Cli(self.__file_path, ipv4="1.2.3.")
        with self.assertRaises(SyntaxError):
            _ = Cli(self.__file_path, ipv4="1.2.3.256")

        self.__clean()

    def test_load_token_from_file(self):
        self.__clean()

        with self.__file_path.open('w') as json_data_file:
            json.dump({"token": self.__test_token}, json_data_file, indent=4)
        client = Cli(config_file_path=self.__file_path)
        client.load_token_from_file()
        self.assertEqual(client.__dict__["_Cli__token"], self.__test_token, "Should be {}".format(self.__test_token))

        self.__clean()

    def __clean(self):
        if self.__file_path.is_file():
            self.__file_path.unlink()


if __name__ == '__main__':
    unittest.main()
