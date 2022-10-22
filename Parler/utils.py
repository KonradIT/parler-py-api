from Parler import with_auth


def add_missing_values(row):
    if "Long" in row and "video.parler.com" in row.get("Long"):
        row["Domain"] = "parler.com"
    return row

def is_ok(data: dict) -> bool:
    return (
        "status" in data and \
        data.get("status") == "success" and \
        "data" in data
    )
def check_login(func):
    def wrapper(*args):
        if not args[0].is_logged_in:
            raise with_auth.AuthSession.NotLoggedIn
        return func(*args)

    return wrapper
