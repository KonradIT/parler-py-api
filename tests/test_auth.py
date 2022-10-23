import Parler
from Parler import with_auth as authed
import os
from Parler import utils
import pytest

p = Parler.Parler(debug=True)
au = authed.AuthSession(debug=False)

def test_auth():
    
    assert not au.is_logged_in
    with pytest.raises(authed.AuthSession.NotLoggedIn):
        au.feed()