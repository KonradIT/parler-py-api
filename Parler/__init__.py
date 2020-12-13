import requests
from typing import List
import random
import string
import json
from time import sleep
import logging
from fake_useragent import UserAgent
import configparser

ua = UserAgent()

class Parler:

    class Errors:
        NoAuth = "Most likely unauthorized or no results"

    @staticmethod
    def get_login_key(email, password):
        data = {
            "identifier": email,
            "password": password,
            "deviceId": "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        }
        response = requests.post("https://api.parler.com/v2/login/new", data=json.dumps(data))
        return response.json()

    @staticmethod
    def get_chapta_image(key):
        data = {
            "identifier": key
        }

        response = requests.post("https://api.parler.com/v2/login/captcha/new", data=json.dumps(data))
        return response.json()

    @staticmethod
    def submit_chapta(key, solution):
        data ={
            "identifier": key,
            "solution":solution
        }

        response = requests.post("https://api.parler.com/v2/login/captcha/submit",data=json.dumps(data))
        return response.json()

    """
    :param jst: short-term token
    :param mst: master token
    :param debug: logging.info debugging messages
    """
    def __init__(self, jst: str, mst: str, debug: bool, config_file: string = None):
        self.jst = jst
        self.mst = mst
        self.debug = debug
        self.base_url = "https://api.parler.com/v1"
        self.session = requests.Session()

        self.session.cookies.set("mst", mst)
        self.session.cookies.set("jst", jst)
        self.session.headers["User-Agent"] = ua.random

        # Default values
        self.reconnects = 0
        self.retry_delay = 2
        self.max_reconnects = 20
        
        if config_file is not None:
            config = configparser.ConfigParser()
            config.read(config_file)
            if "connection" in config and \
                   "retry_delay" in config["connection"] and \
                   "max_reconnects" in config["connection"]:
                self.retry_delay = config["connection"]["retry_delay"]
                self.max_reconnects = config["connection"]["max_reconnects"]

        logging.basicConfig(level=logging.DEBUG if self.debug else logging.ERROR)

    """
    @helper response handler
    pass an http response through to check for specific codes
    """
    def handle_response(self,response):
        if self.reconnects >= self.max_reconnects:
            raise Exception ("Internal abort; {} reconnect attemps".format(self.max_reconnects))
        elif response.status_code >=400 and response.status_code <=428:
            raise Exception ({"status":response.status_code,
                              "error":response.reason,
                             "message": self.Errors.NoAuth})

        elif response.status_code == 502:
            logging.warning(f"Bad Gateway Error, retry in {self.retry_delay} seconds")
            self.reconnects += 1
            sleep(self.retry_delay)

        elif response.status_code == 429:
            logging.warning(f"Too many requests Error, retry in {self.retry_delay} seconds")
            self.reconnects += 1
            sleep(self.retry_delay)

        else:
            self.reconnects = 0

        return response
    
    def get(self, path, **kwargs):
        return self.session.get(self.base_url + path, **kwargs)
    
    def post(self, path, **kwargs):
        return self.session.post(self.base_url + path, **kwargs)
        
    """
    :param username: Username to fetch
    """
    def profile(self, username=None) -> dict:
        response = self.get("/profile")
        if username is not None:
            params = (
                ("username", username),
            )
            response = self.get("/profile", params=params)
        if self.handle_response(response).status_code != 200:
            logging.warning(f"Status: {response.status_code}")
            return self.profile(username)

        return response.json()

    """
    :param searchtag: Hashtag to search
    """
    def hashtags(self, searchtag="") -> dict:
        params = (
            ("search", searchtag),
        )
        response = self.get("/hashtag",  params=params)
        if self.handle_response(response).status_code != 200:
            logging.warning(f"Status: {response.status_code}")
            return self.hashtags(searchtag)
        return response.json()

    """
    :param limit: limit
    :param cursor: string to id the next items
    """
    def feed(self, limit=10, cursor="") -> dict:
        params = (
            ("limit", limit),
        )
        if cursor != "":
            params = params + (("startkey",cursor),)
        response = self.get("/feed",  params=params)
        if self.handle_response(response).status_code != 200:
            logging.warning(f"Status: {response.status_code}")
            return self.feed(limit,cursor)
        return response.json()

    """
    :param item_type: type of created items to list ('post' or 'comment')
    :param username: username to get posts or comments
    :param limit: limit
    :param cursor: string to id the next items
    """
    def created_items(self, item_type="post", username="", limit=10, cursor="") -> dict:
        params = (
            ("username", username),
            ("limit", limit)
        )
        if cursor != "":
            params = params + (("startkey",cursor),)
        response = self.session.get(self.base_url + "/" + item_type + "/creator",  params=params)
        if self.handle_response(response).status_code != 200:
            logging.warning(f"Status: {response.status_code}")
            return self.hashtags(searchtag)
        return response.json()


    """
    :param item_type: type of item to delete ('post' or 'comment')
    :param id: id of item to delete
    """
    def delete_item(self, item_type, id):
        if item_type == 'echo':  # delete echo using post api
            item_type = 'post'
        params = (
            ("id", id),
        )
        response = self.session.post(self.base_url + "/" + item_type + "/delete", params=params)
        if self.handle_response(response).status_code != 200:
            logging.warning(f"Status: {response.status_code}")
        return response.json()

    """
    :param limit: limit
    :param cursor: string to id the next items
    """
    def notifications(self, limit=10, cursor="") -> dict:
        params = (
            ("limit", limit),
        )
        if cursor != "":
            params = params + (("startkey",cursor),)
        response = self.get("/notification",  params=params)
        if self.handle_response(response).status_code != 200:
            logging.warning(f"Status: {response.status_code}")
            return self.notifications(limit, cursor)
        return response.json()

    """
    :param limit: limit
    :param cursor: string to id the next items
    """
    def discover_feed(self, limit=10, cursor="") -> dict:
        params = (
            ("limit", limit),
        )
        if cursor != "":
            params = params + (("startkey",cursor),)
        response = self.get("/discover/posts",  params=params)
        if self.handle_response(response).status_code != 200:
            logging.warning(f"Status: {response.status_code}")
            return self.discover_feed(limit, cursor)
        return response.json()

    """
    :param tag: hashtag to get feed from
    :param limit: limit
    :param cursor: string to id the next items
    """
    def hashtags_feed(self, tag, limit=10, cursor="") -> dict:
        params = (
            ("tag", tag),
            ("limit", limit)
        )
        if cursor != "":
            params = params + (("startkey",cursor),)
        response = self.get("/post/hashtag",  params=params)
        if self.handle_response(response).status_code != 200:
            logging.warning(f"Status: {response.status_code}")
            return self.hashtags_feed(limit, cursor)
        return response.json()
    
    """
    :param creator_id: creator ID from user, NOT username!!
    :param limit: limit
    :param cursor: string to id the next items
    """
    def user_feed(self, creator_id, limit=10, cursor="") -> dict:
        params = (
            ('id', creator_id),
            ('limit', limit),
        )

        if cursor != "":
            params = params + (("startkey",cursor),)
        response = self.get("/post/creator",  params=params)
        if self.handle_response(response).status_code != 200:
            logging.warning(f"Status: {response.status_code}")
            return self.hashtags_feed(limit, cursor)
        return response.json()

    """
    :param search: search term
    """
    def users(self, searchtag="") -> dict:
        params = (
            ("search", searchtag),
        )
        response = self.session.get(self.base_url + "/users", params=params)
        if response.status_code != 200:
            raise Exception({"status": response.status_code})
        return response.json()

    def follow_user(self, username) -> dict:
        params = (
            ("username", username),
        )
        data = json.dumps({"username": username})
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
        }
        response = self.session.post(self.base_url + "/follow", params=params, data=data, headers=headers)
        if response.status_code != 200:
            raise Exception({"status": response.status_code})
        return response.json()