from Parler import with_auth


def add_missing_values(row):
    if "Long" in row and "video.parler.com" in row.get("Long"):
        row["Domain"] = "parler.com"
    return row

def check_login(func):
    def wrapper(*args):
        if not args[0].is_logged_in:
            raise with_auth.AuthSession.NotLoggedIn
        return func(*args)
    return wrapper