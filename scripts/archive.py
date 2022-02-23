import sys, os

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import Parler
from Parler import with_auth as authed
import time, random, datetime, threading
import logging

logging.basicConfig(level=logging.INFO)

from scripts import exputils

required_envs = ["PARLER_USERNAME", "PARLER_PASSWORD"]

for envvar in required_envs:
    assert os.getenv(envvar) != None

parler = Parler.Parler(debug=True)
parler_auth = authed.AuthSession(debug=False)
parler_auth.login(
    identifier=os.getenv("PARLER_USERNAME"), password=os.getenv("PARLER_PASSWORD")
)

assert parler_auth.is_logged_in

r = parler_auth.following(os.getenv("PARLER_USERNAME"), 14)
logging.info("Getting user list")

users = [x.get("username") for x in r]

os.mkdir("data/v2users")
filename = "data/v2users/%s_%s_%s.csv"
max_sleep_limit = 20


def get_posts(username: str):
    print("Starting collection of posts with username %s" % username)
    current_page = 1
    time.sleep(random.randint(1, max_sleep_limit))
    while True:
        try:
            data = parler.user_feed(username, cursor=current_page)
            break
        except Exception as e:
            if e.__class__.__name__ == "TypeError:":
                sys.exit()
            time.sleep(max_sleep_limit)
    with open(
        filename % (username, str(datetime.date.today()), "posts"),
        mode="a",
        encoding="utf-8",
    ) as posts:
        exputils.writetocsv(
            posts,
            [x.get("primary") for x in data.get("data").get("posts")],
            insert_headers=True,
        )

    while True:

        current_page += 1
        time.sleep(random.randint(max_sleep_limit / 2, max_sleep_limit))
        try:
            data = parler.user_feed(username=username, cursor=current_page)
        except Exception as e:
            if e.__class__.__name__ == "TypeError:":
                sys.exit()
            time.sleep(max_sleep_limit)
        finally:
            if "code" in data and data.get("code") == "NO_DATA":
                print("Exiting, all done.")
                break
            with open(
                filename % (username, str(datetime.date.today()), "posts"),
                mode="a",
                encoding="utf-8",
            ) as posts:
                exputils.writetocsv(
                    posts,
                    [x.get("primary") for x in data.get("data").get("posts")],
                    insert_headers=False,
                )

            print("Done page: %s" % current_page)


for user in users:
    thr = threading.Thread(target=get_posts, args=(user,))
    thr.start()
