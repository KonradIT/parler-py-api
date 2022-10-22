import Parler
from Parler import with_auth as authed
import os
import random
from Parler import utils

p = Parler.Parler(debug=True)
au = authed.AuthSession(debug=False)

posts_per_user = 10
search_hits_per_page = 10

badge_types = [
    "gold",
    "rss",
    "private",
    "early",
    "parler_official",
    "verified",
    "parler_emp",
]


def test_get_profile():
    r = p.profile("TheWesternJournal").get("data")
    assert r is not None
    assert "username" in r
    assert (
        "uuid" in r and r.get("uuid") == "40f28d1a-ee94-4d6f-ad9a-ed4cd3a39228"
    )  # https://web.archive.org/web/20220213155807/https://parler.com/open-api/parley.php
    assert "bio" in r
    assert "website" in r
    assert "location" in r
    assert "joined_date" in r
    assert "birthday" in r
    assert "gender" in r
    assert "real_name" in r
    assert "joined_date" in r
    assert "following_count" in r
    assert "follower_count" in r
    assert "is_private" in r
    assert "is_public" in r


def test_get_profile_feed():
    r = p.user_feed(username="TheWesternJournal")
    assert utils.is_ok(r)

    assert len(r.get("data")) == posts_per_user  # posts per user
    assert "postuuid" in r.get("data")[0]
    assert "body" in r.get("data")[0]
    assert "title" in r.get("data")[0]
    assert "total_comments" in r.get("data")[0]
    assert "upvotes" in r.get("data")[0]
    assert "echos" in r.get("data")[0]
    assert "views" in r.get("data")[0]
    assert "is_echo" in r.get("data")[0]
    assert "is_comment" in r.get("data")[0]
    assert "link" in r.get("data")[0]
    assert "trolling" in r.get("data")[0]
    assert "ad" in r.get("data")[0]


def test_get_profile_feed_pagination():
    r1 = p.user_feed(username="TheWesternJournal")
    r2 = p.user_feed(username="TheWesternJournal", cursor=2)
    r3 = p.user_feed(username="TheWesternJournal", cursor=3)

    assert len(r1.get("data")) == posts_per_user
    assert len(r2.get("data")) == posts_per_user
    assert len(r3.get("data")) == posts_per_user

    assert r1.get("data") != r2.get("data")
    assert r2.get("data") != r3.get("data")

    # deep dive: get IDs of each post in user feed, sort alphabetically, compare against n+1

    fp1 = [x.get("postuuid") for x in r1.get("data")]
    fp2 = [x.get("postuuid") for x in r2.get("data")]
    fp3 = [x.get("postuuid") for x in r3.get("data")]

    fp1.sort()
    fp2.sort()
    fp3.sort()

    assert fp1 != fp2
    assert fp2 != fp3


def test_login():
    assert not au.is_logged_in
    assert os.getenv("PARLER_USERNAME") is not None
    assert os.getenv("PARLER_PASSWORD") is not None
    au.login(
        identifier=os.getenv("PARLER_USERNAME"), password=os.getenv("PARLER_PASSWORD")
    )
    assert au.is_logged_in


def test_search_users():
    r = au.users("qanon")
    assert utils.is_ok(r)

    assert len(r.get("data")) == search_hits_per_page

    # pick one at random

    user = r.get("data")[random.randint(0, search_hits_per_page - 1)]

    assert "name" in user
    assert "username" in user
    assert "badges" in user

    for x in badge_types:
        assert x in user.get("badges")
