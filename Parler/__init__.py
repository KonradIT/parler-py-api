import requests
from typing import List, overload
import random
import string
import json
from time import sleep
import logging
from logging.handlers import SocketHandler

from fake_useragent import UserAgent
import configparser
import pipdate
from Parler.version import version

ua = UserAgent()


class Parler:
    class Errors:
        NoAuth = "Most likely unauthorized or no results"

    class UnimplementedException(Exception):
        pass

    class NotSupportedException(Exception):
        pass

    class OldParameterException(Exception):
        pass
    """
    :param debug: logging.info debugging messages
    """

    def __init__(self, debug: bool = False, config_file: string = None):

        # Update check
        p = pipdate.check("parler-api", version)
        if p is not None:
            print(p)

        self.__debug = debug
        self.__base_url = "https://api.parler.com/"
        self.session = requests.Session()

        self.session.get(self.__base_url)
        self.session.headers["User-Agent"] = ua.random

        self.__log = logging.getLogger("parler-py-api")
        self.__log.setLevel(
            level=logging.DEBUG if self.__debug else logging.ERROR)
        self.__log.debug(f"User-Agent: {self.session.headers['User-Agent']}")
        # Default values
        self.__reconnects = 0
        self.__retry_delay = 2
        self.__max_reconnects = 20

        if config_file is not None:
            config = configparser.ConfigParser()
            config.read(config_file)
            if (
                "connection" in config
                and "retry_delay" in config["connection"]
                and "max_reconnects" in config["connection"]
            ):
                self.__retry_delay = config["connection"]["retry_delay"]
                self.__max_reconnects = config["connection"]["max_reconnects"]
            if ["log_to_file"] in "config" and config["log_to_file"][
                "enabled"
            ] == "true":
                fh = logging.FileHandler(config["log_to_file"]["log_file"])
                fh.setLevel(logging.DEBUG)
                self.__log.addHandler(fh)

    """
    @helper response handler
    pass an http response through to check for specific codes
    """

    def handle_response(self, response):
        if self.__reconnects >= self.__max_reconnects:
            raise Exception(
                "Internal abort; {} reconnect attemps".format(
                    self.__max_reconnects)
            )
        elif response.status_code >= 400 and response.status_code <= 428:
            raise Exception(
                {
                    "status": response.status_code,
                    "error": response.reason,
                    "message": self.Errors.NoAuth,
                }
            )

        elif response.status_code == 502:
            self.__log.warning(
                f"Bad Gateway Error, retry in {self.__retry_delay} seconds"
            )
            self.__reconnects += 1
            sleep(self.__retry_delay)

        elif response.status_code == 429:
            self.__log.warning(
                f"Too many requests Error, retry in {self.__retry_delay} seconds"
            )
            self.__reconnects += 1
            sleep(self.__retry_delay)

        else:
            self.__reconnects = 0

        return response

    def get(self, path, **kwargs):
        return self.session.get(self.__base_url + path, **kwargs)

    def post(self, path, **kwargs):
        return self.session.post(self.__base_url + path, **kwargs)

    """
    :param username: Username to fetch
    """

    def profile(self, username: str = "") -> dict:
        response = self.get("v0/public/user/%s" % username)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.profile(username=username)
        return response.json()

    """
    :param limit: limit
    :param cursor: string to id the next items
    """

    def discover_feed(self, limit: int = None, cursor: str = None) -> dict:
        raise self.NotSupportedException()

    """
    :param cursor: cursor
    :param username: username
    """

    def user_feed(self, username: str = "", cursor: int = 1, limit: int = 10, media_only: int = 0) -> dict:
        params = (
            ("page", cursor),
            ("limit", limit),
            ("media_only", media_only)
        )
        response = self.get("v0/public/user/%s/feed" % username, params=params)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.user_feed(cursor=cursor, username=username)
        return response.json()

    """
    param tab: "today" or "top"
    """

    def trending(self, tab: str = "today") -> dict:
        if tab != "today":
            raise self.OldParameterException(
                "%s no longer supported in newer Parler API." % ("tab=top"))

        response = self.get("v0/public/trending/parleys/today")
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.trending()
        return response.json()

    def post_info(self, uuid: str = "") -> dict:
        response = self.get("/v0/public/parleys/%s" % uuid)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.post_info(uuid=uuid)
        return response.json()
