import datetime
import os
import random
import sys
import time
import traceback
import logging
import exputils
import argparse
import continuity_helper

from dotenv import load_dotenv

import csv

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from Parler import Parler, models

load_dotenv(dotenv_path=".parler.env")
parler = Parler(jst=os.getenv("JST"), mst=os.getenv("MST"), debug=True)

filename = "%s/data/usernames/%s_%s_%s.csv"
max_sleep_limit = 6

logging.basicConfig(level=logging.DEBUG)

def get_comments(username, thread_id, output_dir):
    data = parler.comments(thread_id, cursor="")
    feed = models.FeedSchema().load(data)
    while True:
        if feed.last:
            logging.info("Exiting, all done.")
            break
        try:
            data = parler.comments(thread_id, cursor=feed.next)
            feed = models.FeedSchema().load(data)
        except Exception as e:
            if e.__class__.__name__ == "TypeError:":
                sys.exit()
            time.sleep(max_sleep_limit)
        finally:
            logging.info("Writing to file...")
            with open(filename % (output_dir, username + "_" + thread_id, str(datetime.date.today()), "users"), mode="a", encoding="utf-8") as users:
                exputils.writetocsv(users, feed.users, insert_headers=False)
            with open(filename % (output_dir, username + "_" + thread_id, str(datetime.date.today()), "comments"), mode="a", encoding="utf-8") as links:
                exputils.writetocsv(links, feed.links, insert_headers=False)
        time.sleep(random.randint(max_sleep_limit/2, max_sleep_limit))

def get_posts(username, output_dir):
    logging.info("Starting collection of posts from user %s" % username)
    
    while True:
        try:
            userdetails = parler.profile(username)
            data = parler.user_feed(userdetails.get("_id"), 100, cursor="")
            feed = models.FeedSchema().load(data)
            break
        except Exception as e:
            if e.__class__.__name__ == "TypeError:":
                sys.exit()
            time.sleep(max_sleep_limit)
    
    with open(filename % (output_dir, username, str(datetime.date.today()), "posts"), mode="a", encoding="utf-8") as posts:
        exputils.writetocsv(posts, feed.items, insert_headers=True)
    with open(filename % (output_dir, username, str(datetime.date.today()), "links"), mode="a", encoding="utf-8") as links:
        exputils.writetocsv(links, feed.links, insert_headers=True)
    for thread in feed.items:
                get_comments(username=username, thread_id=thread.get("Id"), output_dir=output_dir)
    while True:
        logging.info("is last? %s", feed.last)
        if feed.last:
            logging.info("Exiting, all done.")
            break
        time.sleep(random.randint(1, max_sleep_limit))

        try:
            data = parler.user_feed(
                userdetails.get("_id"), 100, cursor=feed.next)
            feed = models.FeedSchema().load(data)
        except Exception as e:
            traceback.print_exc()
            if e.__class__.__name__ == "TypeError:":
                sys.exit()
            time.sleep(max_sleep_limit)
        finally:
            with open(filename % (output_dir, username, str(datetime.date.today()), "posts"), mode="a", encoding="utf-8") as posts:
                exputils.writetocsv(posts, feed.items)
            with open(filename % (output_dir, username, str(datetime.date.today()), "links"), mode="a", encoding="utf-8") as links:
                exputils.writetocsv(links, feed.links)
            for thread in feed.items:
                get_comments(username=username, thread_id=thread.get("Id"), output_dir=output_dir)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--username', help="username", type=str, required=True, default="TedCruz")
    parser.add_argument(
        '--out', help="out directory", type=str, required=True, default="./")
    args = parser.parse_args()

    get_posts(username=args.username, output_dir=args.out)
