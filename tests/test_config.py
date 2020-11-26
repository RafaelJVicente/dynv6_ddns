import json
import unittest
from pathlib import Path

from dynv6_ddns.config import Config


class TestConfig(unittest.TestCase):
    __file_path = Path("test_dynv6_ddns.json")
    __token = "1234567890"

    def test_default_file_creation(self):
        self.__clean()

        _ = Config(self.__file_path)
        with self.__file_path.open('r') as json_data_file:
            self.assertEqual(json_data_file.readline().rstrip(), "{", "Should be \"{\"")
            second_line = "    \"token\": \"\""
            self.assertEqual(json_data_file.readline().rstrip(), second_line,
                             "Should be {}, where \"_\" means space".format(second_line.replace(' ', '_')))
            self.assertEqual(json_data_file.readline().rstrip(), "}", "Should be \"}\"")

        self.__clean()

    def test_load_config(self):
        self.__clean()

        config = Config(self.__file_path)
        with self.assertRaises(ValueError):
            _ = config.token
        self.__fill_file()
        config.load_config()
        self.assertEqual(config.token, self.__token, "Should be {}".format(self.__token))

        self.__clean()

    def test_token(self):
        self.__clean()

        config = Config(self.__file_path)
        with self.assertRaises(ValueError):
            _ = config.token
        self.__fill_file()
        config = Config(self.__file_path)
        self.assertEqual(config.token, self.__token, "Should be {}".format(self.__token))

        self.__clean()

    def __fill_file(self):
        with self.__file_path.open('w') as json_data_file:
            json.dump({"token": self.__token}, json_data_file, indent=4)

    def __clean(self):
        if self.__file_path.is_file():
            self.__file_path.unlink()


if __name__ == '__main__':
    unittest.main()
