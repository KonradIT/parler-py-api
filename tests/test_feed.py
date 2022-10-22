import Parler
from Parler import with_auth as authed
import os
from Parler import utils

p = Parler.Parler(debug=True)
au = authed.AuthSession(debug=False)

posts_per_feed_page = 10
trending_length = 12
trending_user_length = 20


def test_get_feed():
    assert os.getenv("PARLER_USERNAME") is not None
    assert os.getenv("PARLER_PASSWORD") is not None
    au.login(
        identifier=os.getenv("PARLER_USERNAME"), password=os.getenv("PARLER_PASSWORD")
    )
    assert au.is_logged_in
    assert utils.is_ok(au.feed())
    r1 = au.feed()["data"]
    r2 = au.feed(False, 2, False)["data"]
    r3 = au.feed(False, 3, False)["data"]

    assert len(r1) >= posts_per_feed_page
    assert len(r2) >= posts_per_feed_page-2
    assert len(r3) >= posts_per_feed_page-2

    # deep dive: get IDs of each post in user feed, sort alphabetically, compare against n+1

    fp1 = [x.get("postuuid") for x in r1]
    fp2 = [x.get("postuuid") for x in r2]
    fp3 = [x.get("postuuid") for x in r3]

    fp1.sort()
    fp2.sort()
    fp3.sort()

    assert fp1 != fp2
    assert fp2 != fp3


def test_trending():
    assert len(p.trending("today")["data"]) == trending_length


def test_trending_users():
    assert os.getenv("PARLER_USERNAME") is not None
    assert os.getenv("PARLER_PASSWORD") is not None
    au.login(
        identifier=os.getenv("PARLER_USERNAME"), password=os.getenv("PARLER_PASSWORD")
    )
    assert au.is_logged_in
    assert len(au.trending_users().get("data")) == trending_user_length
