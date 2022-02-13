"""Review user posts and comments, with option to delete after expiration."""
import json
import os
import time
import traceback
import argparse
from datetime import datetime, timedelta
from dotenv import load_dotenv
from termcolor import colored
from Parler import Parler, models

load_dotenv(dotenv_path=".parler.env")
parler = Parler(jst=os.getenv("JST"), mst=os.getenv("MST"), debug=False)


def process_item(item_type, item, expiration, delete_active):
    """Print item summary, after (active or dry run) deleting expired item."""
    # print(json.dumps(item, indent=1))
    time_since = datetime.utcnow() - datetime.strptime(item.get("CreatedAt"),
                                                       "%Y%m%d%H%M%S")
    if expiration is not None and time_since > timedelta(days=expiration):
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


def user_items(username, item_types, expiration=None, delete_active=False):
    """Retrieve posts and comments created by username."""
    if not item_types:
        item_types = ['post', 'comment']
    for item_type in item_types:
        data = parler.created_items(item_type, username, limit=100, cursor="")
        # print(json.dumps(data, indent=1))
        item_key = item_type + 's'
        if item_key not in data.keys() or len(data[item_key]) == 0:
            print('*** no', item_key, 'available for', username)
            continue  # skip processing if no posts/comments
        print('***', item_key, 'for', username)
        # parse comments using same schema as posts
        if "comments" in data.keys():
            data["posts"] = data["comments"].copy()
            del data["comments"]
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
                # parse comments using same schema as posts
                if "comments" in data.keys():
                    data["posts"] = data["comments"].copy()
                    del data["comments"]
                feed = models.FeedSchema().load(data)
                count += 1
            except:
                traceback.print_exc()
                time.sleep(5)
            finally:
                time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p',
                       '--posts',
                       help='only include user posts',
                       dest='item_types',
                       action='append_const',
                       const='post')
    group.add_argument('-c',
                       '--comments',
                       help='only include user comments',
                       dest='item_types',
                       action='append_const',
                       const='comment')
    parser.add_argument(
        '-x',
        '--expiration',
        help='days for user posts/comments to expire, may be fractional',
        type=float)
    parser.add_argument('-D',
                        '--delete',
                        help='delete expired posts/comments, if authorized (otherwise dry run)',
                        action='store_true')  # false if not flagged
    parser.add_argument('users', help='Parler display name(s)', nargs='*')
    args = parser.parse_args()
    for user in args.users:
        user_items(user, args.item_types, args.expiration, args.delete)
