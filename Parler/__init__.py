import requests
from typing import List
import random
import string
import json
from time import sleep

class Parler:


    @staticmethod
    def get_login_key(email, password):
        data = {
            "identifier": email,
            "password": password,
            "deviceId": "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        }
        response = requests.post('https://api.parler.com/v2/login/new', data=json.dumps(data))
        return response.json()
    
    @staticmethod
    def get_chapta_image(key):
        data = {
            "identifier": key
        }

        response = requests.post('https://api.parler.com/v2/login/captcha/new', data=json.dumps(data))
        return response.json()

    @staticmethod
    def submit_chapta(key, solution):
        data ={
            "identifier": key,
            "solution":solution
        }

        response = requests.post('https://api.parler.com/v2/login/captcha/submit',data=json.dumps(data))
        return response.json()
    """
    :param jst: short-term token
    :param mst: master token
    :param debug: print debugging messages
    """
    def __init__(self, jst: str, mst: str, debug: bool):
        self.jst = jst
        self.mst = mst
        self.debug = debug
        self.base_url = "https://api.parler.com/v1"
        self.session = requests.Session()

        self.session.cookies.set("mst", mst)
        self.session.cookies.set("jst", jst)
        self.reconnects = 0

        
    """
    @helper response handler
    pass an http response through to check for specific codes
    """
    
    def handle_response(self,response):
        if self.reconnects >= 10:
            raise Exception ("Internal abort; 10 reconnect attemps")
        elif response.status_code >=400 and response.status_code <=428:
            raise Exception ({'status':response.status_code,
                              'error':response.reason,
                             'English': "Most likely unauthorized or no results"})
            
        elif response.status_code == 502:
            print('Bad Gateway Error, retry in 5 seconds')
            self.reconnects += 1
            sleep(6)

        elif response.status_code == 429:
            print('Too many requests Error, retry in 5 seconds')
            self.reconnects += 1
            sleep(65)

        else:
            self.reconnects = 0

        return response
        
    """
    :param username: Username to fetch
    """
    def profile(self, username=None) -> dict:
        response = self.session.get(self.base_url + "/profile")
        if username is not None:
            params = (
                ("username", username),
            )
            response = self.session.get(self.base_url + "/profile", params=params)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')
            return self.profile(username)

        return response.json()

    """
    :param searchtag: Hashtag to search
    """
    def hashtags(self, searchtag="") -> dict:
        params = (
            ("search", searchtag),
        )
        response = self.session.get(self.base_url + "/hashtag",  params=params)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')

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
        response = self.session.get(self.base_url + "/feed",  params=params)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')

            return self.feed(limit,cursor)
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
        response = self.session.get(self.base_url + "/notification",  params=params)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')

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
        response = self.session.get(self.base_url + "/discover/posts",  params=params)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')

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
        response = self.session.get(self.base_url + "/post/hashtag",  params=params)
        if self.handle_response(response).status_code != 200:
            print(f'Status: {response.status_code}')

            return self.hashtags_feed(limit, cursor)
        return response.json()