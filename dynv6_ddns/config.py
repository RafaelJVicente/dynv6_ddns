import json
from pathlib import Path
from typing import Optional

from dynv6_ddns.types import Token


class Config:
    def __init__(self, file_path: Path = Path.home() / "dynv6_ddns.json"):
        self.__token: Optional[Token] = None
        self.__file_path = file_path
        self.load_config()

    @property
    def token(self) -> Token:
        if not self.__token:
            raise ValueError("Token must be set in config file located in {}".format(self.__file_path.absolute()))
        return self.__token

    def load_config(self):
        if self.__file_path.is_file():
            with self.__file_path.open() as json_data_file:
                data = json.load(json_data_file)
                new_token = data["token"]
                self.__token = new_token if new_token != "" else None
        else:
            self.__token = None
            self.__save_default_config()

    def __save_default_config(self):
        with self.__file_path.open('w') as json_data_file:
            data = {"token": self.__token if self.__token else ""}
            json.dump(data, json_data_file, indent=4)
