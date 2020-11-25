from dotenv import load_dotenv
import json
import time
import os
import sys
import threading
import datetime
import random
sys.path.insert(1, os.path.join(sys.path[0], ".."))
from Parler import Parler, models

load_dotenv(dotenv_path=".parler.env")
parler = Parler(jst=os.getenv("JST"), mst=os.getenv("MST"), debug=False)


hashtags = [
    "voterfraud",
    "electionfraud",
    "StopTheSteal",
    "riggedelection",
    "stopthefraud",
    "electioninterference",
    "electionmeddling",
    "ElectionTampering",
    "electionfraud2020",
    "stolenelection",
    "StopVoterFraud"
    "Election2020",
    "Elections2020",
    "2020Election",
    "2020Elections",
    "Election",
    "Elections",

    "covid19",
    "covid",
    "covid19hoax",
    "covid-19",
    "covidhoax",
    "covid1984",
    "covidexplained",
    "covid19fear",
    "covid_19",
    "covidhoax2020",
    "covidiots",
    "coviddeaths",
    "CovidVaccine",
]
interval = 2
filename = "data/hashtags/%s_%s_%s.json"


def get_posts(hashtag):
    print("Starting collection of posts with hashtag %s" % hashtag)
    time.sleep(random.randint(1, 20))
    while True:
        try:
            data = parler.hashtags_feed(hashtag, 100, cursor="")
            feed = models.FeedSchema().load(data)
            break
        except:
            time.sleep(20)
    while feed.last == False:
        time.sleep(random.randint(1, 20))
        with open(filename % (hashtag, str(datetime.date.today()), "posts"), mode="a") as posts:
            json.dump(feed.items, posts)
        with open(filename % (hashtag, str(datetime.date.today()), "users"), mode="a") as users:
            json.dump(feed.users, users)
        with open(filename % (hashtag, str(datetime.date.today()), "links"), mode="a") as links:
            json.dump(feed.links, links)

        while True:
            try:
                data = parler.hashtags_feed(hashtag, 100, cursor=feed.next)
                feed = models.FeedSchema().load(data)
                break
            except:
                time.sleep(20)


for hashtag in hashtags:
    thr = threading.Thread(target=get_posts, args=(hashtag,))
    thr.start()
