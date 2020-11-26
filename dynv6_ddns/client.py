import re
import time
from pathlib import Path
from threading import Thread
from typing import Union

import requests

from dynv6_ddns.config import Config
from dynv6_ddns.types import Token, IPv4


class Cli:
    def __init__(self, config_file_path: Union[str, Path] = None, token: Token = None,
                 ipv4: IPv4 = None, update_time: int = None):
        self.__config_file_path = Path(config_file_path) if config_file_path else None
        self.__update_time = update_time

        self.__zone_id = None

        if ipv4:
            self.__ipv4 = ipv4
            self.check_ipv4()
        else:
            self.get_current_public_ipv4()

        if token:
            self.__token = token
            self.check_token()
        else:
            self.load_token_from_file()

        self.__thread_active = False
        if update_time:
            self.start_update_thread()

    def get_current_public_ipv4(self):
        # Obtain IPv4
        self.__ipv4 = requests.get('https://api.ipify.org').text.strip()
        self.check_ipv4()

    def update_ipv4(self):
        url = "https://dynv6.com/api/v2/zones/{}".format(self.__zone_id)
        headers = {"Authorization": "Bearer {}".format(self.__token), "Accept": "application/json"}
        params = {"ipv4address": self.__ipv4}
        response = requests.patch(url=url, headers=headers, params=params)
        response.raise_for_status()

    def check_token(self):
        url = "https://dynv6.com/api/v2/zones"
        headers = {"Authorization": "Bearer {}".format(self.__token), "Accept": "application/json"}
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            self.__zone_id = response.json()[0]["id"]
            return
        elif response.status_code == 401:
            raise ValueError("Incorrect token provided")
        else:
            response.raise_for_status()

        raise requests.HTTPError("Request Error: {}".format(response.status_code))

    def check_ipv4(self):
        regex = "(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
        if not re.fullmatch(regex, self.__ipv4):
            raise SyntaxError("IPv4 should have the following format \"xxx.xxx.xxx.xxx\","
                              " where \"xxx\" are numbers between 0 and 255")

    def load_token_from_file(self):
        cfg = Config(self.__config_file_path)
        self.__token = cfg.token
        self.check_token()

    def start_update_thread(self, update_time: int = None):
        if update_time:
            self.__update_time = update_time
        if not self.__update_time:
            raise ValueError("Unknown update_time")
        Thread(target=self.__update_thread).start()

    def stop_update_thread(self, update_time: int = None):
        self.__thread_active = False

    def __update_thread(self):
        self.__thread_active = True
        while self.__thread_active:
            self.get_current_public_ipv4()
            time.sleep(self.__update_time)
