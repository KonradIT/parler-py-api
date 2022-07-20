import Parler
from Parler import with_auth as authed
import os

p = Parler.Parler(debug=True)
au = authed.AuthSession(debug=False)


def test_get_post():
    r = p.post_info("ef4d02fe-7a5a-4ab4-8e82-7c0ee5e32960")
    assert r.get("status") == "ok"

    assert "uuid" in r.get("data")[0].get("primary")
    assert (
        r.get("data")[0].get("primary").get("uuid")
        == "ef4d02fe-7a5a-4ab4-8e82-7c0ee5e32960"
    )
    assert "id" in r.get("data")[0].get("primary")
    assert "uuid" in r.get("data")[0].get("primary")
    assert "body" in r.get("data")[0].get("primary")
    assert "full_body" in r.get("data")[0].get("primary")
    assert "image" in r.get("data")[0].get("primary")
    assert "domain_name" in r.get("data")[0].get("primary")
