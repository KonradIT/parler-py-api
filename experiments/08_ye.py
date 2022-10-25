# Script used to generate graphs and data for the article "Can Ye Save Parler?"

from os import path
import Parler
from Parler import with_auth as authed
import os
from Parler import utils
import time
import datetime
import json
import itertools

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

p = Parler.Parler(debug=True)
au = authed.AuthSession(debug=True)
assert os.getenv("PARLER_USERNAME") is not None
assert os.getenv("PARLER_PASSWORD") is not None

FLAG_WRITE_FILES = True

au.login(
    identifier=os.getenv("PARLER_USERNAME"), password=os.getenv("PARLER_PASSWORD")
)
assert au.is_logged_in

# Hypothesis 1:
# Ye"s followers" creation / joined dates are largely very recent, as in, many people created accounts on parler and followed him after the acquisition announcement.
# Because Parler API does not provide an endpoint to get followers, we gather the comments from his post and check if the commenter follows Ye.
# Unfortunately Ye"s entire list of ~37k followers are out of reach.
# Results:


def Hypothesis1():

    comments = []

    ye_followers_creation_dates = []

    comments_limit = 20
    # Get Ye's posts, which are a few, for now
    r = au.created_items("ye", 20, 1)
    assert utils.is_ok(r)
    for post in r.get("data"):
        cursor = 0
        d = datetime.datetime.now()
        timestamp = d.strftime("%Y-%m-%d %H:%M:%S")

        comments_response = au.comments(
            post.get("postuuid"), cursor, comments_limit, timestamp)
        utils.is_ok(comments_response)
        print(len(comments_response.get("data")))
        comments.append(comments_response.get("data"))
        while utils.is_ok(comments_response) and len(comments_response.get("data")) >= 1:
            cursor += comments_limit
            comments_response = au.comments(
                post.get("postuuid"), cursor, comments_limit, timestamp)
            comments.append(comments_response.get("data"))
            time.sleep(0.5)

    if FLAG_WRITE_FILES:
        with open(path.join("output",  "comments.json"), "w") as f:
            json.dump(comments, f, ensure_ascii=False, indent=4)

    for comment in list(itertools.chain(*comments)):
        cursor = 1

        try:
            r = au.following(comment.get("user").get("username"), 1, 20)
        except:
            continue
        has_found_ye = False
        is_end = False
        while (not has_found_ye) and (not is_end):

            try:
                r = au.following(comment.get(
                    "user").get("username"), cursor, 20)
            except:
                time.sleep(10)
                r = au.following(comment.get(
                    "user").get("username"), cursor, 20)
            if not utils.is_ok(r):
                is_end = True
            if len(r.get("data")) == 0:
                is_end = True
            if utils.is_ok(r) and len(r.get("data")) >= 1:
                following_users = r.get("data")
                for x in following_users:
                    if x.get("username") == "Ye":
                        has_found_ye = True
            cursor += 20
        if has_found_ye:
            try:
                profile_response = p.profile(
                    comment.get("user").get("username"))
                if utils.is_ok(profile_response):
                    ye_followers_creation_dates.append(
                        profile_response.get("data").get("joined_date"))
            except:
                pass

    if FLAG_WRITE_FILES:
        with open(path.join("output",  "ye_followers_creation_dates.json"), "w") as f:
            json.dump(ye_followers_creation_dates, f,
                      ensure_ascii=False, indent=4)

    # Make a chart

    # aggregate by date
    dates_agg = {}

    for x in sorted(ye_followers_creation_dates):

        parsed = x.split("T")[0]
        if parsed not in dates_agg:
            dates_agg[parsed] = 0
        dates_agg[parsed] += 1

    dataframe_dates = pd.to_datetime(list(dates_agg.keys()))
    dataframe_amounts = list(dates_agg.values())

    fig = plt.figure(figsize=(10, 7))
    fig.tight_layout()
    plt.xticks(rotation=90)
    plt.plot(dataframe_dates, dataframe_amounts)
    plt.title("Ye's Parler Account's Followers' creation dates")

    plt.ylabel("Amount")
    ax = plt.gca()
    days_fmt = mdates.DateFormatter("%D")
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.xaxis.set_major_formatter(days_fmt)
    ax.set_xlim([datetime.date(2022, 9, 1), datetime.date(2022, 10, 25)])
    ax.axvline(datetime.date(2022, 10, 17), ls="-", color="red",
               label="Parler Purchase Announcement (17/10)")
    plt.gca().legend()
    plt.savefig("chart.png")


Hypothesis1()
