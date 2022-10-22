import Parler
from Parler import with_auth as authed
import os
from Parler import utils

p = Parler.Parler(debug=True)
au = authed.AuthSession(debug=False)


def test_get_post():
    r = p.post_info("ef4d02fe-7a5a-4ab4-8e82-7c0ee5e32960")
    assert utils.is_ok(r)
    assert "postuuid" in r.get("data")
    assert (
        r.get("data").get("postuuid")
        == "ef4d02fe-7a5a-4ab4-8e82-7c0ee5e32960"
    )
    assert "body" in r.get("data")
