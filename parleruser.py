"""Delete posts and comments created before expiration deadline."""
import json
import os
import time
import traceback
from datetime import datetime, timedelta
from dotenv import load_dotenv
from termcolor import colored
from Parler import Parler, models

load_dotenv(dotenv_path=".parler.env")
parler = Parler(jst=os.getenv("JST"), mst=os.getenv("MST"), debug=False)


def process_item(item_type, item, expiration, delete_active):
    """Delete expired item if expired, then print item report."""
    # print(json.dumps(item, indent=1))
    time_since = datetime.utcnow() - datetime.strptime(item.get("CreatedAt"),
                                                       "%Y%m%d%H%M%S")
    if expiration and time_since > timedelta(days=float(expiration)):
        date_color = "red"
        deletion_msg = " ***DELETING*** "
        if delete_active:
            try:
                deletion_msg += parler.delete_item(item_type,
                                                   item.get("Id"))["message"]
            except Exception as e:
                deletion_msg += e.args[0]['error']
        else:
            deletion_msg += "Dry run"
    else:
        date_color = "green"
        deletion_msg = ""
    if item_type == "post":
        body_color = "blue"
    else:
        body_color = "yellow"
    print("\t", colored(item.get("Id"), "cyan"))
    print(
        "\t>>> Created:",
        colored(
            item.get("CreatedAt") + " (" + str(time_since) + ")" +
            deletion_msg, date_color))
    print("\t>>>",
          item_type.capitalize() + ":",
          colored(item.get("Body").replace("\n", " "), body_color))


def user_items(username, expiration=None, delete_active=False):
    """Retrieve posts and comments created by username."""
    for item_type in ['post', 'comment']:
        data = parler.created_items(item_type, username, limit=100, cursor="")
        if len(data[item_type + 's']) == 0:
            break  # skip processing if no posts/comments
        feed = models.FeedSchema().load(data)
        count = 0
        while count < 20:
            try:
                for item in feed.items:
                    process_item(item_type, item, expiration, delete_active)
                if feed.last:
                    break
                more_items = feed.next
                data = parler.created_items(item_type,
                                            username,
                                            limit=100,
                                            cursor=more_items)
                feed = models.FeedSchema().load(data)
                count += 1
            except:
                traceback.print_exc()
                time.sleep(5)
            finally:
                time.sleep(1)


if __name__ == '__main__':
    username = os.getenv("USERNAME")  # display name
    expiration = os.getenv("EXPIRATION")  # days, may be fractional
    user_items(username, expiration)
