from re import sub
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
        self.__log = self._Parler__log

    class NotLoggedIn(Exception):
        pass

    def login(self, identifier: str, password: str) -> dict:

        data = json.dumps(
            {"identifier": identifier, "password": password, "device_id": ""}
        )
        response = self.post(
            "/functions/sessions/authentication/login/login.php", data=data
        )
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.login(identifier=identifier, password=password)
        self.__log.debug("Logged in")
        return response.json()

    @property
    def is_logged_in(self):
        return self.session.cookies.get("parler_auth_token") not in [None, ""]

    """
    Functions that require authentication but are non-signed-user facing
    """

    """
    :param hide_echoes: Hide Parler retweets (echoes)
    :param cursor: id to the next items
    :param subscriptions_only: subscriptions only
    """

    @check_login
    def feed(
        self,
        hide_echoes: bool = False,
        cursor: int = 1,
        subscriptions_only: bool = False,
    ) -> dict:
        files = {
            "page": (None, cursor),
            "hide_echoes": (None, hide_echoes),
            "subscriptions_only": (None, subscriptions_only),
        }
        response = self.post("api/MainFeedEndpoint.php", files=files)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.feed(
                hide_echoes=hide_echoes,
                cursor=cursor,
                subscriptions_only=subscriptions_only,
            )
        return response.json()

    """
    :param searchtag: search term
    """

    @check_login
    def users(self, searchtag: str = "") -> dict:
        files = {"s": (None, searchtag), "type": (None, "user")}
        response = self.post("pages/search-results.php", files=files)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.users(searchtag=searchtag)
        return response.json()

    """
    :param searchtag: Hashtag to search
    """

    @check_login
    def hashtags(self, searchtag="") -> dict:
        files = {"s": (None, searchtag), "type": (None, "hashtags")}
        response = self.post("pages/search-results.php", files=files)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.hashtags(searchtag=searchtag)
        return response.json()

    """
    :param tag: hashtag to get feed from
    """

    @check_login
    def hashtags_feed(self, tag) -> dict:
        files = {
            "tag": (None, tag),
        }
        response = self.post("pages/hashtags.php", files=files)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.hashtags_feed(tag=tag)
        return response.json()

    """
    :param username: username
    :param cursor: cursor
    """

    @check_login
    def followers(self, creator_id, limit=10, cursor="") -> dict:
        raise self.NotSupportedException

    """
    :param username: username
    :param cursor: cursor
    """

    @check_login
    def trending_users(self):
        response = self.post("functions/trending_users.php")
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.trending_users()
        return response.json()

    @check_login
    def following(self, username: str = "", cursor: int = 1) -> dict:
        files = {
            "page": (None, cursor),
            "user": (None, username),
        }
        response = self.post("pages/profile/following-results.php", files=files)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.following(cursor=cursor, username=username)
        return response.json()

    """
    :param post_id: post id
    :param cursor: cursor
    """

    @check_login
    def comments(self, post_id: str = "", cursor: int = 0) -> dict:
        params = (
            ("post_id", post_id),
            ("page", cursor),
        )
        response = self.get("functions/post_comments.php", params=params)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.comments(post_id=post_id, cursor=cursor)
        return response.json()

    """
    Functions that require authentication for interfacing with the current signed in user
    """

    def __user_interactions_helper(self, params: dict = {}) -> dict:

        response = self.get("functions/user_interactions.php", params=params)
        if self.handle_response(response).status_code != 200:
            self.__log.warning(f"Status: {response.status_code}")
            return self.__user_interactions_helper(params=params)
        return response.json()

    """
    :param username: username
    """

    @check_login
    def follow_user(self, username) -> dict:
        params = (
            ("user", username),
            ("action", "follow"),
        )
        return self.__user_interactions_helper(params=params)

    @check_login
    def unfollow_user(self, username) -> dict:
        params = (
            ("user", username),
            ("action", "unfollow"),
        )
        return self.__user_interactions_helper(params=params)

    """
    :param item_type: type of created items to list ("post" or "comment")
    :param username: username to get posts or comments
    :param limit: limit
    :param cursor: string to id the next items
    """

    @check_login
    def created_items(self, item_type="post", username="", limit=10, cursor="") -> dict:
        return self.UnimplementedException

    """
    :param item_type: type of item to delete ("post" or "comment")
    :param id: id of item to delete
    """

    @check_login
    def delete_item(self, item_type, id):
        return self.UnimplementedException

    """
    :param limit: limit
    :param cursor: string to id the next items
    """

    @check_login
    def notifications(self, limit=10, cursor="") -> dict:
        return self.UnimplementedException
