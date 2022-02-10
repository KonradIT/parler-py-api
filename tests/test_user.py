import Parler
from Parler import with_auth as authed
import os
p = Parler.Parler(debug=True)
au = authed.AuthSession(debug=False)

posts_per_user = 20

def test_get_profile():
    r = p.profile("TheWesternJournal")
    assert r is not None
    assert "username" in r
    assert "dateCreated" in r
    assert ("uuid" in r and r.get("uuid") == "40f28d1a-ee94-4d6f-ad9a-ed4cd3a39228")
    assert "bio" in r 
    assert "website" in r
    assert "location" in r
    assert "joinedAt" in r


def test_get_profile_feed():
    r = p.user_feed(username="TheWesternJournal")
    assert len(r.get("data").get("posts")) == posts_per_user # posts per user
    assert "id" in r.get("data").get("posts")[0].get("primary")
    assert "uuid" in r.get("data").get("posts")[0].get("primary")
    assert "body" in r.get("data").get("posts")[0].get("primary")
    assert "full_body" in r.get("data").get("posts")[0].get("primary")
    assert "image" in r.get("data").get("posts")[0].get("primary")
    assert "domain_name" in r.get("data").get("posts")[0].get("primary")

def test_login():
    assert not au.is_logged_in
    au.login(
        identifier=os.getenv("PARLER_USERNAME"),
        password=os.getenv("PARLER_PASSWORD")
    )
    assert au.is_logged_in
