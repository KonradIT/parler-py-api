from dotenv import load_dotenv
import json
import time
import os
import datetime
import sys
import exputils
import random
import logging

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from Parler import Parler, models

load_dotenv(dotenv_path=".parler.env")
parler = Parler(jst=os.getenv("JST"), mst=os.getenv("MST"), debug=False)

max_sleep_limit= 6
filename = "data/comment_chain_%s_%s_%s.csv"
comment_id = sys.argv[1]
logging.basicConfig(level=logging.DEBUG)

data = parler.comments(comment_id, cursor="")
feed = models.FeedSchema().load(data)
while True:
	if feed.last:
		logging.info("Exiting, all done.")
		break
	try:
		data = parler.comments(comment_id, cursor=feed.next)
		feed = models.FeedSchema().load(data)
	except Exception as e:
		if e.__class__.__name__ == "TypeError:":
			sys.exit()
		time.sleep(max_sleep_limit)
	finally:
		logging.info("Writing to file...")
		with open(filename % (comment_id, str(datetime.date.today()), "users"), mode="a", encoding="utf-8") as users:
			exputils.writetocsv(users, feed.users, insert_headers=False)
		with open(filename % (comment_id, str(datetime.date.today()), "comments"), mode="a", encoding="utf-8") as links:
			exputils.writetocsv(links, feed.links, insert_headers=False)
	time.sleep(random.randint(max_sleep_limit/2, max_sleep_limit))
