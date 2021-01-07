from dotenv import load_dotenv
import json
import time
import os
import datetime
import sys
import signal

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from Parler import Parler, models

load_dotenv(dotenv_path=".parler.env")
parler = Parler(jst=os.getenv("JST"), mst=os.getenv("MST"), debug=False)

interval = 2
filename = "data/stopthesteal_11_09-10.json"
if len(sys.argv) > 1:
	filename = sys.argv[1]

data = parler.hashtags_feed("stopthesteal", 100, cursor="")
feed = models.FeedSchema().load(data)

while feed.last == False:
	time.sleep(interval)
	# for i in feed.items:
	# 	if i.get("Id2") == "84d168ce1cb94114a7cb3d4f17a30ae0": exit()
	with open(filename, mode="a", encoding="utf-8") as posts:
		json.dump(feed.items, posts)
	try:
		data = parler.hashtags_feed("stopthesteal", 100, cursor=feed.next)
		feed = models.FeedSchema().load(data)
	except:
		time.sleep(20)
		data = parler.hashtags_feed("stopthesteal", 100, cursor=feed.next)
		feed = models.FeedSchema().load(data)
print("File needs cleaning up....")