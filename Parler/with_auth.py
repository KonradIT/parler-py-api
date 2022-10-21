from re import sub
from typing import Optional
from Parler import Parler
import json
import string
from Parler.utils import check_login


class AuthSession(Parler):

    """
    Functions for logging in - which require initialization
    """

    def __init__(self, debug: bool = False, config_file: string = None):
        super().__init__(debug, config_file)
        self.__credentials = {
            "access_token": "",
            "refresh_token": ""
        }

    class NotLoggedIn(Exception):
        pass

    def login(self, identifier: str, password: str) -> dict:

        data = (
            {"identifier": identifier, "password": password}
        )
        response = self.post("v0/login", json=data)

        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.login(identifier=identifier, password=password)

        received = response.json()
        self.__credentials["access_token"] = received["access_token"]
        self.__credentials["refresh_token"] = received["refresh_token"]

        self.session.headers["Authorization"] = "Bearer " + \
            received["access_token"]
        return response.json()

    @property
    def is_logged_in(self):
        return self.__credentials["refresh_token"] != ""

    """
    Functions that require authentication but are non-signed-user facing
    """

    """
    :param hide_echoes: Hide Parler retweets (echoes) !DEPRECATED
    :param cursor: id to the next items
    :param subscriptions_only: subscriptions only !DEPRECATED
    :param limit: limit entries

    """

    @check_login
    def feed(
        self,
        hide_echoes: bool = False,
        cursor: int = 1,
        subscriptions_only: bool = False,
        limit: int = 10
    ) -> Optional[dict]:

        if hide_echoes or subscriptions_only:
            raise self.OldParameterException("%s no longer supported in newer Parler API." % (
                "hide_echoes" if hide_echoes else ("subscriptions_only" if subscriptions_only else "")))

        params = (
            ("page", cursor),
            ("limit", limit),
        )
        response = self.get("v0/parleys/feed/dashboard", params=params)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.feed(
                cursor=cursor,
                limit=limit
            )
        return response.json()

    """
    :param searchtag: search term
    """

    @check_login
    def users(self, searchtag: str = "", cursor: int = 1, limit: int = 10) -> dict:
        params = (
            ("page", cursor),
            ("limit", limit),
        )
        response = self.get("v0/search/user/%s" % searchtag, params=params)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.users(searchtag=searchtag)
        return response.json()

    """
    :param searchtag: Hashtag to search
    """

    @check_login
    def hashtags(self, searchtag="", cursor: int = 1, limit: int = 10) -> dict:
        params = (
            ("page", cursor),
            ("limit", limit),
        )
        response = self.get("v0/search/hashtag/%s" % searchtag, params=params)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.hashtags(searchtag=searchtag)
        return response.json()

    """
    :param tag: hashtag to get feed from
    """

    @check_login
    def hashtags_feed(self, tag) -> dict:
        raise self.NotSupportedException()
    """
    :param username: username
    :param cursor: cursor
    """

    @check_login
    def followers(self, creator_id, limit=10, cursor="") -> dict:
        raise self.NotSupportedException()

    """
    :param username: username
    :param cursor: cursor
    """

    @check_login
    def trending_users(self):
        response = self.get("v0/trending/users/today")
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.trending_users()
        return response.json()

    @check_login
    def following(self, username: str = "", cursor: int = 1,  limit: int = 20) -> dict:
        params = (
            ("page", cursor),
            ("limit", limit),
        )
        response = self.get("v0/user/%s/following" % username, params=params)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.following(username=username, cursor=cursor, limit=limit)
        return response.json()

    """
    :param post_id: post id
    :param cursor: cursor
    """

    @check_login
    def comments(self, post_id: str = "", cursor: int = 0, limit: int = 10, timestamp: str = "") -> dict:
        params = (
            ("offset", cursor),
            ("limit", limit),
            ("timestamp", timestamp),
        )
        response = self.get("v0/parleys/%s/comments_before/" %
                            post_id, params=params)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.comments(post_id=post_id, cursor=cursor, limit=limit, timestamp=timestamp)
        return response.json()

    @check_login
    def post_info(self, post_id: str = "") -> dict:
        response = self.get("v0/parleys/%s" % post_id)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.post_info(post_id=post_id)
        return response.json()

    """
    :param username: username
    """

    @check_login
    def follow_user(self, username) -> dict:
        raise self.NotSupportedException()

    @check_login
    def unfollow_user(self, username) -> dict:
        raise self.NotSupportedException()

    """
    :param item_type: type of created items to list ("post" or "comment")
    :param username: username to get posts or comments
    :param limit: limit
    :param cursor: string to id the next items
    """

    @check_login
    def created_items(self, username="", limit=10, cursor="", media_only: int = 0) -> dict:
        params = (
            ("page", cursor),
            ("limit", limit),
            ("media_only", media_only)
        )
        response = self.get("v0/user/%s/feed/" % username, params=params)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.following(username=username, cursor=cursor, limit=limit)
        return response.json()

    """
    :param item_type: type of item to delete ("post" or "comment")
    :param id: id of item to delete
    """

    @check_login
    def delete_item(self, item_type, id):
        raise self.UnimplementedException()

    """
    :param limit: limit
    :param cursor: string to id the next items
    """

    @check_login
    def notifications(self, limit=10, cursor="") -> dict:
        raise self.UnimplementedException()
